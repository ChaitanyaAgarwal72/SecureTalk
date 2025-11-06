import socket
import threading
import struct

clients = []

def recvall(sock, n):
    """Receive exactly n bytes."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    clients.append(conn)

    while True:
        try:
            raw_len = recvall(conn, 4)
            if not raw_len:
                break
            msg_len = struct.unpack('>I', raw_len)[0]

            msg = recvall(conn, msg_len)
            if not msg:
                break

            for client in clients:
                if client != conn:
                    try:
                        client.send(struct.pack('>I', len(msg)) + msg)
                    except:
                        clients.remove(client)

        except:
            break

    print(f"[-] Connection closed: {addr}")
    clients.remove(conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen()
    print("[*] SecureTalk Server started on port 9999...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
