import socket
import threading
import struct
from encryption_utils import encrypt_message, decrypt_message, generate_shared_key

shared_key = generate_shared_key()
print("[*] Using shared ASCON-AEAD128 key for this session.")

def recvall(sock, n):
    """Receive exactly n bytes."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_messages(sock):
    while True:
        try:
            raw_len = recvall(sock, 4)
            if not raw_len:
                break
            msg_len = struct.unpack('>I', raw_len)[0]

            encrypted_msg = recvall(sock, msg_len)
            if encrypted_msg:
                try:
                    decrypted_msg = decrypt_message(shared_key, encrypted_msg)
                    print(f"\nFriend: {decrypted_msg}")
                except Exception as e:
                    print(f"\n[!] Failed to decrypt message: {e}")
                    print(f"[DEBUG] Message length: {len(encrypted_msg)} bytes")
            else:
                break
        except:
            print("[!] Connection lost.")
            break

def send_message(sock, encrypted_msg):
    """Send message with length prefix."""
    sock.sendall(struct.pack('>I', len(encrypted_msg)) + encrypted_msg)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    print("[*] Connected to SecureTalk Server.")
    print("Type messages below (type 'exit' to quit):\n")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input("")
        if msg.lower() == "exit":
            client.close()
            print("[*] Disconnected.")
            break

        encrypted_msg = encrypt_message(shared_key, msg)
        send_message(client, encrypted_msg)
        print(f"You: {msg}")

if __name__ == "__main__":
    main()
