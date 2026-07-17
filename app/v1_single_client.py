import socket

def handle_client(sock, addr):
    try:
        while True:
            # recv(4096) = reads upto 4096 bytes. BLOCKS if no data
            data = sock.recv(4096)

            # Empty bytes means the client has closed the connection
            if not data:
                print(f"{addr} has disconnected")
                break

            print(f"{addr} sent: {data.decode()}")
            # Echo it back
            # sendall() ensures ALL bytes are sent
            # send() might send partial data if buffer is full
            sock.sendall(data)
    finally:
        sock.close() # Always close the connection, even if an error occured

def main():
    # Creating a TCP/IPv4 socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow port reuse to prevent 'Address already in use'
    # because after close() the port enters TIME_WAIT for ~ 60 seconds
    # SO_REUSEADDR lets us bind immediately without waiting
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # '' means 0.0.0.0 = accept connections on ANY network interface and bind to all interfaces on port 8000
    server_socket.bind(('', 8000))

    # Starts listening and will hold up to 5 pending connections
    server_socket.listen(5)
    print('Echo server listening on port 8000 ...')

    while True:
        # BLOCKS until a client connects
        # Returns a NEW socket for this specific client + their address
        client_socket, client_addr = server_socket.accept()
        print(f"Connection from {client_addr}")

        # Handle the client, meaning BLOCK on recv -- no other client should be able to connect
        handle_client(client_socket, client_addr)

if __name__ == "__main__":
    main()
