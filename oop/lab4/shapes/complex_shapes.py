from .simple_shapes import LineShape, RectShape
from .mixins import CircleEndsMixin, CubeFrameMixin

class LineWithCircles(LineShape, CircleEndsMixin):
    def draw(self, canvas):
        super().draw(canvas)
        self.draw_circle_ends(canvas)

class CubeFrame(RectShape, CubeFrameMixin):
    def draw(self, canvas):
        self.draw_cube_frame(canvas)
