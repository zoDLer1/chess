from settings.gamesettings import MAP_WIDTH, MAP_HEIGHT
from .mixins import DefaultPointRendererMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from directions.direction import Direction


class PointRenderer:

    def __init__(self, figure):
        self.figure = figure

    def render_direction(self, direction: 'Direction', max):
        current_column, current_row = self.figure.column, self.figure.row

        while True:
            current_column, current_row, = direction.get_next(current_column, current_row)
            row_in_map = MAP_WIDTH >= current_row + 1 and current_row + 1 > 0
            column_in_map = MAP_HEIGHT >= current_column + 1 and current_column + 1 > 0
            delta = max >= abs(current_column - self.figure.column) and max >= abs(current_row - self.figure.row)
            
            if row_in_map and column_in_map and delta:
                object = self.figure.map.get_figure(current_column, current_row)
                if object:
                    self.on_object(object, direction, current_column, current_row)
                else:
                    self.on_empty_field(direction, current_column, current_row)
            else:
                break    


class DefaultPointRenderer(PointRenderer, DefaultPointRendererMixin):
    pass

    

