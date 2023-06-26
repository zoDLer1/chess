from game_objects.base import GameObject
from directions.direction import DirectionManager, Direction
from game_objects.points import Point, AttackPoint, CastlingPoint
from typing import TYPE_CHECKING
from settings.gamesettings import MAP_WIDTH, MAP_HEIGHT


if TYPE_CHECKING:
    from map import Map


class Figure(GameObject):

    max = 7
    directions = DirectionManager()


    def update_direction(self):
        for direction in self.directions:
            self.update_fields_ty_direction(direction, self.get_max())

    def update_fields_ty_direction(self, direction: Direction, max):
        current_column, current_row = self.column, self.row
        
        while True:
            current_column, current_row, = direction.get_next(current_column, current_row)
            row_in_map = MAP_WIDTH >= current_row + 1 and current_row + 1 > 0
            column_in_map = MAP_HEIGHT >= current_column + 1 and current_column + 1 > 0
            delta = max >= abs(current_column - self.column) and max >= abs(current_row - self.row)
            
            if row_in_map and column_in_map and delta:
                self.fields.add((current_column, current_row))

    def get_max(self):
        return self.max
    
    def update_position(self, column, row):
        self.column = column
        self.row = row

    def get_path(self):
        return super().get_path().format(color=self.color)

    def __init__(self, map: 'Map', column: int, row: int, color: str):
        self.points = []
        self.fields = set()
        self.color = color
        super().__init__(map, column, row)

    def moveToPoint(self, point: Point):
        self.moveToPosition(point.column, point.row, point.relative_direction)

    def moveToPosition(self, column, row, direction):
        x, y = self.map.get_coords(column, row)
        self.map.movement(self, x, y, direction)

    def onObjectClicked(self):
        for direction in self.directions:
            self.render_points(direction, self.get_max())

    def render_points(self, direction: Direction, max, context={}):
        current_column, current_row = self.column, self.row
        
        while True:
            current_column, current_row, = direction.get_next(current_column, current_row)
            row_in_map = MAP_WIDTH >= current_row + 1 and current_row + 1 > 0
            column_in_map = MAP_HEIGHT >= current_column + 1 and current_column + 1 > 0
            delta = max >= abs(current_column - self.column) and max >= abs(current_row - self.row)
            
            if row_in_map and column_in_map and delta:
                object = self.map.get_field(current_column, current_row)
                if (object):
                    if (isinstance(object, Figure)):
                        
                        self.onObject(object, direction, current_column, current_row, context)
                    break
                else:
                    self.onEmptyField(direction, current_column, current_row, context)           
            else:
                break
    
    def destroy_points(self):
        for point in self.points:
            point.destroy()
        self.points = []

    def onObject(self, object: 'Figure', direction: Direction, column: int, row: int, context):
        if (object.color != self.color):
            AttackPoint(self, direction, object, column, row)

    def onEmptyField(self, direction, column, row, context):
        Point(self, direction, column, row)

class Pawn(Figure):
    max = 1
    dash_max = 2
    directions = DirectionManager(Direction.n())
    path = r'images/figures/{color}/P.png'

    def __init__(self, map: 'Map', column: int, row: int, color: str):
        super().__init__(map, column, row, color)
        self.dash = True

    def onObjectClicked(self):
        super().onObjectClicked()
        super().render_points(Direction.ne(), 1, True)
        super().render_points(Direction.nw(), 1, True)
    
    def onObject(self, object: 'Figure', direction: Direction, column: int, row: int, context):
        if context:
            return super().onObject(object, direction, column, row, context)

    def onEmptyField(self, direction: Direction, column, row, context):
        if not context:
            return super().onEmptyField(direction, column, row, context)

    def update_position(self, column, row):
        if row == 0:
            self.promotion(column, row)
        else:
            super().update_position(column, row)

    def moveToPoint(self, point: 'Point'):
        super().moveToPoint(point)        
        self.dash = False

    def promotion(self, column, row):
        self.destroy()
        Queen(self.map, column, row, self.color)

    def get_max(self):
        return self.dash_max if self.dash else self.max
  
class Rook(Figure):
    directions = DirectionManager.lines()
    path = r'images/figures/{color}/R.png'

class Queen(Figure):
    directions = DirectionManager.star()
    path = r'images/figures/{color}/Q.png'

class Bishop(Figure):
    directions = DirectionManager.diagonals()
    path = r'images/figures/{color}/B.png'

class Knight(Figure):
    max = 2
    directions = DirectionManager.circle()
    path = r'images/figures/{color}/N.png'

class King(Figure):
    max = 1
    directions = DirectionManager.star()
    path = r'images/figures/{color}/K.png'

    def __init__(self, map: 'Map', column: int, row: int, color: str):
        self.has_castling = True
        super().__init__(map, column, row, color)


    def moveToPosition(self, column, row, direction):
        self.has_castling = False
        return super().moveToPosition(column, row, direction)

    def onObjectClicked(self):
        if self.has_castling:
            super().render_points(Direction.w(), MAP_WIDTH - 1, True)
            super().render_points(Direction.e(), MAP_WIDTH - 1, True)
        super().onObjectClicked()

    def onEmptyField(self, direction: Direction, column, row, context):
        if not context:
            return super().onEmptyField(direction, column, row, context)
        
    def onObject(self, object: Figure, direction: Direction, column: int, row: int, context):
        if not context:
            return super().onObject(object, direction, column, row, context)
        else:
            if isinstance(object, Rook):
                CastlingPoint(self, direction, object, object.column, object.row)
            
            
