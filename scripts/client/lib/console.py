import socket

class Console:
    def __init__(self, host = '127.0.0.1', port = 8001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()
        print('Python got a client at {}'.format(self.address))

    def recv(self):
        self.buffer = self.connection.recv(1024).decode()
        return self.buffer

    def send(self, msg):
        _ = self.connection.send(msg.encode())

    def close(self):
        _ = self.connection.close()