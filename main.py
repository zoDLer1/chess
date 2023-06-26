from app import App
from map import Map

if __name__ == '__main__':
    app = App()
    
    map = Map(app)
    app.mainloop()