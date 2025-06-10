import socket
import time

# Constants
SERVER_IP = '127.0.0.1'   # Server IP address (localhost for testing)
SERVER_PORT = 8080        # Server port to connect to
REQUEST_FILE = 'index.html' # The file that the client will request from the server

def start_client(server_ip, server_port, file_name):
    """
    Establishes a connection to the server, sends a GET request for a specified file,
    receives the response, and calculates the Round-Trip Time (RTT).
    """
    try:
        # Create a socket object for TCP connection (IPv4, Stream socket)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Start high-precision timer to calculate RTT
        start_time = time.perf_counter()  # Record start time in seconds (high precision)

        # Connect to the server using IP address and port
        client_socket.connect((server_ip, server_port))

        # Calculate RTT by measuring the time after connection
        rtt = (time.perf_counter() - start_time) * 1000  # Convert RTT to milliseconds

        # Prepare the HTTP GET request to request the specified file from the server
        request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        
        # Send the request encoded in UTF-8 format to the server
        client_socket.sendall(request.encode('utf-8'))

        # Receive the response from the server (up to 4096 bytes)
        response = client_socket.recv(4096).decode('utf-8')

        # Print the server's response
        print(f"Response from server:\n{response}")

        # Print the calculated Round-Trip Time in milliseconds, formatted to 2 decimal places
        print(f"Round-Trip Time (RTT): {rtt:.2f} ms")

    finally:
        # Close the socket connection to the server
        client_socket.close()

# Entry point of the script
if __name__ == "__main__":
    # Start the client by connecting to the server IP and port and requesting the specified file
    start_client(SERVER_IP, SERVER_PORT, REQUEST_FILE)
