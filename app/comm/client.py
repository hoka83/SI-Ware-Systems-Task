import socket


class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def receive(self):
        if self.sock:
            return self.sock.recv(1024).decode()
        return ""

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
