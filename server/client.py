import socket
from settings.appsettings import HOST, PORT

class Client:
    
    
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))



    # def accept_client(self):
    #     while True:
    #         user = self.server.accept()
    #         client, address = user
    #         print(client, address)
    #         # info = client.recv(1024).decode('utf-8')
    #         # request = self.parse_headers(info, user)
    #         client.shutdown(socket.SHUT_WR)
