import argparse
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000


def run_client(client_id, host, port, messages):
    try:
        with socket.create_connection((host, port)) as sock:
            print(f"[client {client_id}] connected to {host}:{port}")

            for msg in messages:
                sock.sendall(msg.encode())
                data = sock.recv(4096)
                print(f"[client {client_id}] sent: {msg!r}  ->  received: {data.decode()!r}")

        print(f"[client {client_id}] connection closed")
    except OSError as e:
        print(f"[client {client_id}] failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Simulate one or more concurrent TCP echo clients")
    parser.add_argument("messages", nargs="*", default=["hello", "world", "bye"],
                         help="Messages each client sends, in order")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--clients", type=int, default=1,
                         help="Number of concurrent client connections to spawn")
    args = parser.parse_args()

    threads = [
        threading.Thread(target=run_client, args=(i + 1, args.host, args.port, args.messages))
        for i in range(args.clients)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
