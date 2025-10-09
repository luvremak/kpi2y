import math
from .base import Shape

class Star(Shape):
    def draw(self, canvas):
        points = self._calculate_star_points()
        canvas.create_polygon(points, outline='black', fill='yellow', width=2)

    def draw_rubber(self, canvas):
        points = self._calculate_star_points()
        canvas.create_polygon(points, outline='black', fill='', width=1)

    def _calculate_star_points(self):
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        r_outer = min(abs(self.x2 - self.x1), abs(self.y2 - self.y1)) / 2
        r_inner = r_outer * 0.4

        points = []
        for i in range(10):
            angle = math.pi / 2 + (2 * math.pi * i / 10)
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            points.extend([x, y])
        return points
