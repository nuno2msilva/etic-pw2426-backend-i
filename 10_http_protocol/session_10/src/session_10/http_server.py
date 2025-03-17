import socket

# Define the host and port to listen on
HOST, PORT = '127.0.0.1', 8080

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate reuse of address after program exit
    server_socket.bind((HOST, PORT)) # Bind the socket to the host and port
    server_socket.listen(1) # Listen for incoming connections
    print(f"Serving HTTP on {HOST} port {PORT} ...")

    while True:
        client_connection, client_address = server_socket.accept() # Accept a new client connection
        with client_connection:
            request_data = client_connection.recv(1024).decode('utf-8') # Receive the request data (limit to 1024 bytes for simplicity)
            print("Received request:")
            print(request_data)

            # Construct a simple HTTP response
            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: 46\r\n"
                "\r\n"
                "<html><body><h1>Hello, HTTP!</h1></body></html>"
            )

            # Send the HTTP response back to the client
            client_connection.sendall(http_response.encode('utf-8'))