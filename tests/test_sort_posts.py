import requests
import time
import subprocess
import os
import signal

def test_sort_posts():
    # Start the backend
    backend_process = subprocess.Popen(['python3', 'backend/backend_app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start

    base_url = "http://localhost:5002/api/posts"

    try:
        # 1. Test default order
        response = requests.get(base_url)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
        print("Default order test passed")

        # 2. Test sort by title asc
        response = requests.get(f"{base_url}?sort=title&direction=asc")
        assert response.status_code == 200
        data = response.json()
        titles = [post["title"] for post in data]
        assert titles == sorted(titles)
        print("Sort by title asc test passed")

        # 3. Test sort by title desc
        response = requests.get(f"{base_url}?sort=title&direction=desc")
        assert response.status_code == 200
        data = response.json()
        titles = [post["title"] for post in data]
        assert titles == sorted(titles, reverse=True)
        print("Sort by title desc test passed")

        # 4. Test sort by content asc
        response = requests.get(f"{base_url}?sort=content&direction=asc")
        assert response.status_code == 200
        data = response.json()
        contents = [post["content"] for post in data]
        assert contents == sorted(contents)
        print("Sort by content asc test passed")

        # 5. Test invalid sort field
        response = requests.get(f"{base_url}?sort=invalid")
        assert response.status_code == 400
        assert "Invalid sort field" in response.json()["error"]
        print("Invalid sort field test passed")

        # 6. Test invalid direction
        response = requests.get(f"{base_url}?sort=title&direction=wrong")
        assert response.status_code == 400
        assert "Invalid direction" in response.json()["error"]
        print("Invalid direction test passed")

        print("All sorting tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")
        os.kill(backend_process.pid, signal.SIGTERM)
        raise e
    finally:
        os.kill(backend_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_sort_posts()
