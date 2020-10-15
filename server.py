import socket
import sys
import configparser

def getaddr():
    conf = configparser.ConfigParser()
    conf.read_file(open('key.conf'))
    host = conf.get('connection','host')
    port = conf.get('connection','port')
    return (host,port)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_addr = getaddr()
    server.bind(serv_addr)
    print(f"[+] Listening on {serv_addr[0]}:{serv_addr[1]}")
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