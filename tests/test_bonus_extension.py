import requests

BASE_URL = "http://localhost:5002/api/posts"

def test_add_post_with_new_fields():
    print("Testing add post with author and date...")
    new_post = {
        "title": "New Post",
        "content": "This is a new post.",
        "author": "Alice",
        "date": "2023-06-10"
    }
    response = requests.post(BASE_URL, json=new_post)
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Alice"
    assert data["date"] == "2023-06-10"
    print("PASSED")

def test_add_post_validation():
    print("Testing add post validation...")
    # Missing author
    incomplete_post = {"title": "T", "content": "C", "date": "2023-01-01"}
    response = requests.post(BASE_URL, json=incomplete_post)
    assert response.status_code == 400
    assert "Missing fields: author" in response.json()["error"]

    # Invalid date
    invalid_date_post = {"title": "T", "content": "C", "author": "A", "date": "not-a-date"}
    response = requests.post(BASE_URL, json=invalid_date_post)
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["error"]
    print("PASSED")

def test_update_post_new_fields():
    print("Testing update post with author and date...")
    update_data = {"author": "Bob", "date": "2023-06-11"}
    response = requests.put(f"{BASE_URL}/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["author"] == "Bob"
    assert data["date"] == "2023-06-11"
    print("PASSED")

def test_search_by_new_fields():
    print("Testing search by author and date...")
    # Add a post first to ensure we have something to search for
    requests.post(BASE_URL, json={"title": "Search T", "content": "Search C", "author": "Charlie", "date": "2023-07-01"})
    
    # Search by author
    response = requests.get(f"{BASE_URL}/search?author=charlie")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["author"] == "Charlie"

    # Search by date
    response = requests.get(f"{BASE_URL}/search?date=2023-07-01")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["date"] == "2023-07-01"
    print("PASSED")

def test_sort_by_date():
    print("Testing sort by date...")
    # Add posts with different dates
    requests.post(BASE_URL, json={"title": "A", "content": "C", "author": "A", "date": "2023-01-01"})
    requests.post(BASE_URL, json={"title": "B", "content": "C", "author": "A", "date": "2023-12-31"})
    requests.post(BASE_URL, json={"title": "C", "content": "C", "author": "A", "date": "2023-06-15"})

    # Sort ASC
    response = requests.get(f"{BASE_URL}?sort=date&direction=asc")
    assert response.status_code == 200
    dates = [post["date"] for post in response.json()]
    assert dates == sorted(dates)

    # Sort DESC
    response = requests.get(f"{BASE_URL}?sort=date&direction=desc")
    assert response.status_code == 200
    dates = [post["date"] for post in response.json()]
    assert dates == sorted(dates, reverse=True)
    print("PASSED")

if __name__ == "__main__":
    try:
        test_add_post_with_new_fields()
        test_add_post_validation()
        test_update_post_new_fields()
        test_search_by_new_fields()
        test_sort_by_date()
        print("\nAll bonus extension tests passed!")
    except AssertionError as e:
        print(f"\nTest failed!")
        raise e
