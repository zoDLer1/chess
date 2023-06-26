from settings.gamesettings import GAME_SIZE 
from PIL import Image, ImageTk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map import Map


Images = []


class GameObject:
    
    path = None

    def get_path(self):
        return self.path

    def onObjectClicked():
        pass
    
    def __init__(self, map: 'Map', column: int, row: int):
        self.map = map
        self.row = row
        self.column = column
        self.set_image()
        self.obj_id = self.map.set_field(self.column, self.row, self)

    def destroy(self):
        self.map.remove_field_value(self.column, self.row, self.obj_id)
        Images.remove(self.img)
        
    def set_image(self):
        img = Image.open(self.get_path())
        img.thumbnail((GAME_SIZE, GAME_SIZE))
        self.img = ImageTk.PhotoImage(img)
        Images.append(self.img)

    def __str__(self) -> str:
        return f'<"{self.__class__.__name__}" object at ({self.row}, {self.column})>'





