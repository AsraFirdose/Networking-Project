import socket
import threading
import os
import time

# Constants
HOST = '127.0.0.1'  # Localhost IP address
PORT = 8080         # Port number to run the server on

def handle_client(client_socket, client_address):
    """
    Handles the incoming client request.
    Parses the request, retrieves the requested file, and sends the appropriate HTTP response.
    """
    try:
        # Receive the client's request (up to 1024 bytes) and decode it from bytes to string
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Request from {client_address}:\n{request}")

        # Split the request into lines for easy parsing
        lines = request.splitlines()
        if len(lines) > 0:
            # Extract the request line (e.g., "GET /index.html HTTP/1.1")
            request_line = lines[0]
            parts = request_line.split()
            
            # Check if request is a valid GET request
            if len(parts) >= 2 and parts[0] == 'GET':
                # Get the requested file name by removing the leading '/'
                file_name = parts[1].lstrip('/')
                
                # Check if the requested file exists in the directory
                if os.path.isfile(file_name):
                    # If file exists, read file content in binary mode
                    with open(file_name, 'rb') as file:
                        content = file.read()
                    
                    # Create HTTP 200 OK response header
                    response = b"HTTP/1.1 200 OK\r\n"
                    response += b"Content-Type: text/html\r\n\r\n" + content
                else:
                    # If file does not exist, send HTTP 404 Not Found response
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                    response += b"<h1>404 Not Found</h1>"
            else:
                # If the request is not properly formatted, send HTTP 400 Bad Request response
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
                response += b"<h1>400 Bad Request</h1>"
        else:
            # Send 400 response if the request line is empty
            response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
            response += b"<h1>400 Bad Request</h1>"

        # Send the generated response to the client
        client_socket.sendall(response)
    finally:
        # Close the client socket connection after response is sent
        client_socket.close()

def start_server(port=PORT):
    """
    Initializes and starts the server, listening for incoming connections.
    Spawns a new thread for each connected client.
    """
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified host and port
    server_socket.bind((HOST, port))
    
    # Start listening for incoming connections (up to 5 clients can queue)
    server_socket.listen(5)
    print(f"Server started on port {port}. Waiting for connections...")

    # Continuously accept incoming connections
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")
        
        # Handle the client connection in a new thread
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_handler.start()  # Start the thread, allowing for parallel connections

# Entry point for the server script
if __name__ == "__main__":
    start_server()  # Start the server on the specified port
