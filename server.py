import socket
import sys

host = '127.0.0.1'
port = 5003

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    print(f"[+] Listening on {host}:{port}")
    server.listen()
    try:
        while True:
            clientsocket, addr = server.accept()
            print(f"[+] Got connection from {addr[0]}:{addr[1]}")
            data = clientsocket.recv(1024)
            print(data.decode("utf-8"))
    except KeyboardInterrupt:
        server.close()
        print("[!] Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()