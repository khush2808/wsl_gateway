#!/usr/bin/env python3
import socket
import threading
import sys


def get_wsl_ip():
    """Find WSL IP address by checking common WSL network ranges"""
    common_ranges = ["172.16.0.0/12", "192.168.0.0/16"]

    # Try to connect to common WSL ports to discover IP
    test_ports = [8000, 22, 80]

    for port in test_ports:
        try:
            # Try connecting to localhost:port through WSL
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", port))
            sock.close()

            if result == 0:
                return "localhost"
        except:
            pass

    return None


def forward_data(source, destination):
    """Forward data between source and destination sockets"""
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except:
        pass
    finally:
        source.close()
        destination.close()


def handle_client(client_socket, target_host, target_port):
    """Handle incoming client connection"""
    try:
        # Connect to target server
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((target_host, target_port))

        # Create threads for bidirectional forwarding
        thread1 = threading.Thread(
            target=forward_data, args=(client_socket, target_socket)
        )
        thread2 = threading.Thread(
            target=forward_data, args=(target_socket, client_socket)
        )

        thread1.daemon = True
        thread2.daemon = True

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_gateway(listen_port, target_host, target_port):
    """Start the gateway server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(("0.0.0.0", listen_port))
        server.listen(5)
        print(f"Gateway listening on 0.0.0.0:{listen_port}")
        print(f"Forwarding to {target_host}:{target_port}")
        print("Press Ctrl+C to stop")

        while True:
            client_socket, addr = server.accept()
            print(f"New connection from {addr}")

            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, target_host, target_port)
            )
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\nShutting down gateway...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    import time

    # Forwarding rules: (listen_port, target_host, target_port)
    rules = [
        (3000, "localhost", 8000),
        (3001, "localhost", 8006)
    ]

    print("Starting port forwarding...")

    threads = []
    for listen_port, target_host, target_port in rules:
        t = threading.Thread(
            target=start_gateway,
            args=(listen_port, target_host, target_port)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down gateways...")

