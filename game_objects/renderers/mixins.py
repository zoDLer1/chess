from game_objects.points import AttackPoint, Point, CastlingPoint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from directions.direction import Direction
    from game_objects.figures import Figure


class BaseRendererMixin:
    def on_object(self, *args):
        pass

    def on_empty_field(self, *args):
        pass

class AttackPointsOnlyRendererMixin(BaseRendererMixin):

    def on_object(self, object: 'Figure', direction: 'Direction', column: int, row: int):
        if (object.color != self.figure.color): 
            # not isinstance(object, King)
            AttackPoint(self.figure, direction, object, column, row)

class PointsOnlyRendererMixin(BaseRendererMixin):

    def on_empty_field(self, direction: 'Direction', column: int, row: int):
        Point(self.figure, direction, column, row)

class DefaultPointRendererMixin(PointsOnlyRendererMixin, AttackPointsOnlyRendererMixin):
    pass
                                                
    