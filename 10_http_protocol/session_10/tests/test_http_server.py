import subprocess
import socket
import time
import pytest

@pytest.fixture(scope="module")
def server():
    # Start the server as a subprocess
    server_process = subprocess.Popen(
        ["python", "server.py"],  # Replace with your script's filename
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for the server to start
    max_retries = 10
    for _ in range(max_retries):
        try:
            with socket.create_connection(('127.0.0.1', 8080), timeout=1):
                break
        except (ConnectionRefusedError, OSError):
            time.sleep(0.2)
    else:
        pytest.fail("Server did not start within the expected time")
    yield server_process
    # Terminate the server process after tests
    server_process.terminate()
    try:
        server_process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        server_process.kill()

def test_http_response(server):
    # Connect to the server and send a test request
    with socket.create_connection(('127.0.0.1', 8080), timeout=5) as client_socket:
        # Send an HTTP GET request
        client_socket.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        # Receive the response
        response = client_socket.recv(1024)
    
    # Validate the response
    assert b"HTTP/1.1 200 OK" in response
    assert b"Content-Type: text/html; charset=utf-8" in response
    assert b"Hello, HTTP!" in response