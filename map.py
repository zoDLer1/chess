from tkinter import Canvas
from settings.appsettings import FPS
from settings.gamesettings import GAME_SIZE, MAP_WIDTH, MAP_HEIGHT, MOVE_SPEED, ANIMATIONS
from constants.colors import BLACK, WHITE
from typing import TYPE_CHECKING
from game_objects.figures import Pawn, Figure, Queen, Bishop, Rook, King, Knight

if TYPE_CHECKING:
    from directions.direction import Direction
    from game_objects.base import GameObject
    


class ChessBoard:

    def __init__(self, root) -> None:
        self.fields = []
        self.active = None
        self.has_action = False
        self.root = root
        self.render()

    def movement(self, obj: 'Figure', x, y, direction: 'Direction'):
        self.has_action = True
        current_x, current_y = self.canvas.coords(obj.obj_id)
        if (current_x != x or current_y != y) and ANIMATIONS:
            self.canvas.move(obj.obj_id, MOVE_SPEED * direction.up, MOVE_SPEED * direction.left)
            self.canvas.after(int(1000 / FPS), lambda: self.movement(obj, x, y, direction))
        else:
            self.canvas.coords(obj.obj_id, x,y)
            column, row = self.get_field_coords(x, y)
            self.fields[obj.column][obj.row] = None
            self.fields[column][row] = obj
            obj.update_position(column, row)
            self.has_action = False

    def render(self):
        self.canvas = Canvas(self.root, bg='lightblue', highlightthickness=0, width=GAME_SIZE * MAP_WIDTH, height=GAME_SIZE * MAP_HEIGHT)
        self.canvas.pack(anchor='w')
        x = 0
        y = 0
        for row in range(0, MAP_WIDTH):
            row_fields = []
            for column in range(0, MAP_HEIGHT):
                self.canvas.create_rectangle(
                    x, y, x + GAME_SIZE, y + GAME_SIZE, fill=self.get_field_color(row, column), width=0)
                row_fields.append(None)
                x = x + GAME_SIZE
            self.fields.append(row_fields)
            y = y + GAME_SIZE
            x = 0
        self.canvas.bind_all('<Button-1>', self.on_click)
        self.spawn()

    def spawn(self):
        Pawn(self, 1, 2, BLACK)
        Queen(self, 5, 5, BLACK)
        King(self, 4, 7, WHITE)
        # Bishop(self, 5, 7, WHITE)
        # Knight(self, 3, 3, WHITE)
        # Rook(self, 0, 7, WHITE)
        # Rook(self, 7, 7, WHITE)

    @staticmethod
    def get_field_color(column, row):
        return WHITE if (row-column) % 2 == 0 else BLACK

    def get_field(self, column, row):
        return self.fields[column][row]

    def get_figure(self, current_column, current_row):
        object = self.get_field(current_column, current_row)
        if object and isinstance(object, Figure):
            return object
        


    def on_click(self, evt):
        if not self.has_action:
            x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
            y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
            row, column = self.get_field_coords(x, y)
            object = self.fields[row][column]
            
            if self.active:
                self.active.destroy_points()
                self.active = None
            
            if object:    
                print(object)
                if isinstance(object, Figure):
                    self.active = object
                object.on_object_clicked()

    def remove_field_value(self, column, row, obj_id):
        self.fields[column][row] = None
        self.canvas.delete(obj_id)

    def set_field(self, column, row, value: 'GameObject'):
        self.update_field(column, row, value)
        return self.canvas.create_image(*self.get_coords(column, row), image=value.img)

    def update_field(self, column, row, value: 'GameObject'):
        self.fields[column][row] = value

    @staticmethod
    def get_field_coords(x, y):
        return (int(x//GAME_SIZE), int(y//GAME_SIZE))

    @staticmethod
    def get_coords(column, row):
        x = GAME_SIZE / 2
        y = GAME_SIZE / 2
        if column != 0:
            x = x + GAME_SIZE * column
        if row != 0:
            y = y + GAME_SIZE * row
        return (x, y)
