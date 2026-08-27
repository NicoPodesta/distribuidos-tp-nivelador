import socket


def recv_all(sock: socket.socket, size: int) -> bytes:
    data = bytearray()

    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            raise ConnectionResetError("Socket closed before receiving all requested bytes")
        data.extend(packet)

    return bytes(data)


def send_all(sock: socket.socket, bytes: bytes) -> None:
    bytes_sent = 0

    while bytes_sent < len(bytes):
        sent = sock.send(bytes[bytes_sent:])
        if sent == 0:
            raise RuntimeError("Failed to write to socket: 0 bytes sent")
        bytes_sent += sent
