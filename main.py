from app import App
from map import ChessBoard
from server import Server, Client

if __name__ == '__main__':
    # Server()
    # Client()
    
    app = App()
    
    map = ChessBoard(app)
    app.mainloop()