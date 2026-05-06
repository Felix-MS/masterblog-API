from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/masterblog.json"  # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'  # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Set the path to the JSON file
# Use an absolute path to avoid issues with different working directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, 'posts.json')


def load_posts():
    """
    Load posts from the JSON file.
    """
    if not os.path.exists(POSTS_FILE):
        return []
    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_posts(posts):
    """
    Save posts to the JSON file.
    """
    try:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=4)
    except IOError:
        pass


def find_next_id():
    """
    Find the next available ID for a new post.
    """
    posts = load_posts()
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Get all posts, optionally sorted by title, content, author or date.
    """
    posts = load_posts()
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    # Valid options
    valid_sort_fields = ['title', 'content', 'author', 'date']
    valid_directions = ['asc', 'desc']

    # If no sorting is requested, return the original list
    if not sort_field:
        return jsonify(posts)

    # Validate sort field
    if sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field: {sort_field}. Valid fields are: {', '.join(valid_sort_fields)}"}), 400

    # Validate direction
    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction: {direction}. Valid directions are: {', '.join(valid_directions)}"}), 400

    # Create a sorted copy of the posts
    reverse = (direction == 'desc')
    try:
        if sort_field == 'date':
            # Sort by actual date object
            sorted_posts = sorted(posts, key=lambda x: datetime.strptime(x.get(sort_field, "1970-01-01"), "%Y-%m-%d"), reverse=reverse)
        else:
            sorted_posts = sorted(posts, key=lambda x: x.get(sort_field, "").lower(), reverse=reverse)
    except (KeyError, ValueError, AttributeError):
        # Handle cases where date format might be wrong or field is missing or not a string
        return jsonify(posts)

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new post to the JSON file.
    """
    posts = load_posts()
    data = request.get_json()

    # Validation
    required_fields = ['title', 'content', 'author', 'date']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Date format validation
    try:
        datetime.strptime(data['date'], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_id = find_next_id()
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content'],
        "author": data['author'],
        "date": data['date']
    }
    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    Delete a post from the JSON file.
    """
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    posts = [post for post in posts if post['id'] != id]
    save_posts(posts)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Update an existing post in the JSON file.
    """
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    data = request.get_json()

    # Update fields if provided
    if 'title' in data:
        post['title'] = data['title']

    if 'content' in data:
        post['content'] = data['content']

    if 'author' in data:
        post['author'] = data['author']

    if 'date' in data:
        # Date format validation if updating date
        try:
            datetime.strptime(data['date'], "%Y-%m-%d")
            post['date'] = data['date']
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    save_posts(posts)
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title, content, author and/or date.
    """
    posts = load_posts()
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    author_query = request.args.get('author', '').lower()
    date_query = request.args.get('date', '').lower()

    filtered_posts = []

    for post in posts:
        match = True
        if title_query and title_query not in post['title'].lower():
            match = False
        if content_query and content_query not in post['content'].lower():
            match = False
        if author_query and author_query not in post['author'].lower():
            match = False
        if date_query and date_query not in post['date'].lower():
            match = False
        
        if match:
            filtered_posts.append(post)

    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
