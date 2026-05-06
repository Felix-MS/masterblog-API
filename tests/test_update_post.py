import requests
import time
import subprocess
import os
import signal

def test_update_post():
    # Start the backend
    backend_process = subprocess.Popen(['python3', 'backend/backend_app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Wait for server to start

    base_url = "http://localhost:5002/api/posts"

    try:
        # 1. Test updating both title and content
        payload = {"title": "Updated Title", "content": "Updated Content"}
        response = requests.put(f"{base_url}/1", json=payload)
        print(f"Update all fields - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated Content"

        # 2. Test updating only title
        payload = {"title": "Only Title Updated"}
        response = requests.put(f"{base_url}/1", json=payload)
        print(f"Update only title - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Updated"
        assert data["content"] == "Updated Content"  # Should remain same

        # 3. Test updating only content
        payload = {"content": "Only Content Updated"}
        response = requests.put(f"{base_url}/2", json=payload)
        print(f"Update only content - Status Code: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert data["title"] == "Second post"  # Should remain same
        assert data["content"] == "Only Content Updated"

        # 4. Test updating non-existent post
        payload = {"title": "Irrelevant"}
        response = requests.put(f"{base_url}/999", json=payload)
        print(f"Update non-existent post - Status Code: {response.status_code}")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

        print("All update tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")
        os.kill(backend_process.pid, signal.SIGTERM)
        raise e
    finally:
        os.kill(backend_process.pid, signal.SIGTERM)

if __name__ == "__main__":
    test_update_post()
