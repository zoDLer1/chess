import socket
from settings.appsettings import HOST, PORT

class Server:
    

    
    def __init__(self) -> None:
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()
        self.accept_client()

    def accept_client(self):
        accepting = True
        while accepting:
            user = self.server.accept()
            client, address = user
            self.clients.append(client)
            print(f'Connected with address {address}')
            if (len(self.clients) == 2):
                pass
            # info = client.recv(1024).decode('utf-8')

            


            # 
            # request = self.parse_headers(info, user)
            # client.shutdown(socket.SHUT_WR)
