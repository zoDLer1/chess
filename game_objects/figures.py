from game_objects.base import GameObject
from directions.direction import DirectionManager, Direction
from game_objects.points import Point, AttackPoint, CastlingPoint
from typing import TYPE_CHECKING
from settings.gamesettings import MAP_WIDTH, MAP_HEIGHT
from .renderers.renderers import DefaultPointRenderer

if TYPE_CHECKING:
    from map import ChessBoard

class Figure(GameObject):

    max = 7
    directions = DirectionManager()

    def get_max(self):
        return self.max
    
    def update_position(self, column, row):
        self.column = column
        self.row = row

    def get_path(self):
        return super().get_path().format(color=self.color)

    def __init__(self, map: 'ChessBoard', column: int, row: int, color: str):
        self.points = []
        self.fields = set()
        self.color = color
        self.point_renderer = DefaultPointRenderer(self)
        super().__init__(map, column, row)

    def move_to_point(self, point: Point):
        self.move_to_position(point.column, point.row, point.relative_direction)

    def move_to_position(self, column, row, direction):
        x, y = self.map.get_coords(column, row)
        self.map.movement(self, x, y, direction)

    def on_object_clicked(self):
        for direction in self.directions:
            self.render_points(direction, self.get_max())

    def render_points(self, direction: Direction, max):
        self.point_renderer.render_direction(direction, max)
    
    def destroy_points(self):
        for point in self.points:
            point.destroy()
        self.points = []

    # def on_object(self, object: 'Figure', direction: Direction, column: int, row: int):
    #     if (object.color != self.color and not isinstance(object, King)):
    #         AttackPoint(self, direction, object, column, row)

    # def on_empty_field(self, direction, column, row):
    #     Point(self, direction, column, row)

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

    def __init__(self, map: 'ChessBoard', column: int, row: int, color: str):
        self.has_castling = True
        super().__init__(map, column, row, color)

    

    def move_to_position(self, column, row, direction):
        self.has_castling = False
        return super().move_to_position(column, row, direction)

    def on_object_clicked(self):
        if self.has_castling:
            super().render_points(Direction.w(), MAP_WIDTH - 1, True)
            super().render_points(Direction.e(), MAP_WIDTH - 1, True)
        super().on_object_clicked()

    def on_empty_field(self, direction: Direction, column, row, context):
        if not context:
            return super().on_empty_field(direction, column, row, context)
        
    def on_object(self, object: Figure, direction: Direction, column: int, row: int, context):
        if not context:
            return super().on_object(object, direction, column, row, context)
        else:
            if isinstance(object, Rook):
                CastlingPoint(self, direction, object, object.column, object.row)

class Pawn(Figure):
    max = 1
    dash_max = 2
    directions = DirectionManager(Direction.n())
    path = r'images/figures/{color}/P.png'

    def __init__(self, map: 'ChessBoard', column: int, row: int, color: str):
        super().__init__(map, column, row, color)
        self.dash = True

    def on_object_clicked(self):
        super().on_object_clicked({'render_attack_points': False, 'render_points': True})
        super().render_points(Direction.ne(), 1, {'render_attack_points': True, 'render_points': False})
        super().render_points(Direction.nw(), 1, {'render_attack_points': True, 'render_points': False})
    
    def on_object(self, object: 'Figure', direction: Direction, column: int, row: int, context):
        if context['render_attack_points']:
            return super().on_object(object, direction, column, row, context)

    def on_empty_field(self, direction: Direction, column, row, context):
        if context['render_points']:
            return super().on_empty_field(direction, column, row, context)

    def update_position(self, column, row):
        if row == 0:
            self.promotion(column, row)
        else:
            super().update_position(column, row)

    def move_to_point(self, point: 'Point'):
        super().move_to_point(point)        
        self.dash = False

    def promotion(self, column, row):
        self.destroy()
        Queen(self.map, column, row, self.color)

    def get_max(self):
        return self.dash_max if self.dash else self.max
  