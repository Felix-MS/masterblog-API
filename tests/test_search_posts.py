import requests
import time
import subprocess
import os
import signal

def test_search_posts():
    # Start the backend
    backend_process = subprocess.Popen(['python3', 'backend/backend_app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start

    base_url = "http://localhost:5002/api/posts/search"

    try:
        # 1. Test search by title
        response = requests.get(f"{base_url}?title=first")
        print(f"Search title 'first' - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "First post" in data[0]["title"]

        # 2. Test search by content
        response = requests.get(f"{base_url}?content=second")
        print(f"Search content 'second' - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Second post" in data[0]["title"]

        # 3. Test search by both title and content
        response = requests.get(f"{base_url}?title=post&content=first")
        print(f"Search title 'post' and content 'first' - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 1

        # 4. Test search with no matches
        response = requests.get(f"{base_url}?title=nonexistent")
        print(f"Search title 'nonexistent' - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

        # 5. Test search with no parameters (should return all posts)
        response = requests.get(base_url)
        print(f"Search no params - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        print("All search tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")
        os.kill(backend_process.pid, signal.SIGTERM)
        raise e
    finally:
        os.kill(backend_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_search_posts()
