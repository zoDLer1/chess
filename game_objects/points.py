from game_objects.base import GameObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.figures import Figure
    from directions.direction import Direction


class Point(GameObject):
    path = r'images/points/point.png'
   
    def __init__(self, owner: 'Figure', direcrion: 'Direction', column: int, row: int):
        super().__init__(owner.map, column, row)
        self.relative_direction = direcrion
        self.owner = owner
        self.owner.points.append(self)

    def on_object_clicked(self):
        self.owner.move_to_point(self)

class AttackPoint(Point):
    path = r'images/points/attack_point.png'

    def __init__(self, owner: 'Figure', direction: 'Direction', target: 'Figure', column: int, row: int):
        super().__init__(owner, direction, column, row)
        self.target = target

    def destroy(self):
        super().destroy()
        self.map.update_field(self.column, self.row, self.target)
    
    def on_object_clicked(self):
        super().on_object_clicked()
        self.target.destroy()

class CastlingPoint(AttackPoint):
    path = r'images/points/castle_point.png'
    def on_object_clicked(self):
        if self.relative_direction.up > 0:
            self.owner.move_to_position(self.owner.column + 1, self.owner.row, self.relative_direction)
            self.target.move_to_position(self.target.column - 3, self.target.row, self.relative_direction.reverse())
        elif self.relative_direction.up < 0:
            self.owner.move_to_position(self.owner.column - 2, self.owner.row, self.relative_direction)
            self.target.move_to_position(self.target.column + 3, self.target.row, self.relative_direction.reverse())
   
