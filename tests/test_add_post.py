import requests
import time
import subprocess
import os
import signal

def test_add_post():
    # Start the backend
    backend_process = subprocess.Popen(['python3', 'backend/backend_app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start

    base_url = "http://localhost:5002/api/posts"

    try:
        # 1. Test adding a valid post
        payload = {"title": "New Post", "content": "New Content"}
        response = requests.post(base_url, json=payload)
        print(f"Test Success - Status Code: {response.status_code}")
        if response.status_code == 201:
            print(f"Response Body: {response.json()}")
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "New Post"
        assert data["content"] == "New Content"

        # 2. Test missing title
        payload = {"content": "Content Only"}
        response = requests.post(base_url, json=payload)
        print(f"Test Missing Title - Status Code: {response.status_code}")
        assert response.status_code == 400

        # 3. Test missing content
        payload = {"title": "Title Only"}
        response = requests.post(base_url, json=payload)
        print(f"Test Missing Content - Status Code: {response.status_code}")
        assert response.status_code == 400

        # 4. Verify post was actually added
        response = requests.get(base_url)
        posts = response.json()
        print(f"Total posts: {len(posts)}")
        assert any(p["title"] == "New Post" for p in posts)
        print("All tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")
        # Clean up process before raising
        os.kill(backend_process.pid, signal.SIGTERM)
        raise e
    finally:
        os.kill(backend_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_add_post()
