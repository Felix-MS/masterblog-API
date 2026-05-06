import requests
import time
import subprocess
import os
import signal

def test_delete_post():
    # Start the backend
    backend_process = subprocess.Popen(['python3', 'backend/backend_app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start

    base_url = "http://localhost:5002/api/posts"

    try:
        # 1. Verify initial posts (id 1 and 2 exist)
        response = requests.get(base_url)
        posts = response.json()
        print(f"Initial posts: {len(posts)}")
        assert any(p['id'] == 1 for p in posts)

        # 2. Test deleting an existing post (id 1)
        response = requests.delete(f"{base_url}/1")
        print(f"Delete existing post - Status Code: {response.status_code}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # 3. Verify post was actually deleted
        response = requests.get(base_url)
        posts = response.json()
        print(f"Posts after deletion: {len(posts)}")
        assert all(p['id'] != 1 for p in posts)

        # 4. Test deleting a non-existent post (id 999)
        response = requests.delete(f"{base_url}/999")
        print(f"Delete non-existent post - Status Code: {response.status_code}")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

        print("All delete tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")
        os.kill(backend_process.pid, signal.SIGTERM)
        raise e
    finally:
        os.kill(backend_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_delete_post()
