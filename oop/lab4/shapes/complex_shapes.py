from .simple_shapes import LineShape, RectShape
from .mixins import CircleEndsMixin, CubeFrameMixin


class LineWithCircles(LineShape, CircleEndsMixin):
    def draw(self, canvas):
        super().draw(canvas)
        self.draw_circle_ends(canvas)

    def draw_rubber(self, canvas):
        ids = []
        line_id = super().draw_rubber(canvas)
        if line_id is not None:
            if isinstance(line_id, (list, tuple)):
                ids.extend(line_id)
            else:
                ids.append(line_id)
        circle_ids = self.draw_circle_ends_rubber(canvas)
        if circle_ids:
            if isinstance(circle_ids, (list, tuple)):
                ids.extend(circle_ids)
            else:
                ids.append(circle_ids)
        return ids


class CubeFrame(RectShape, CubeFrameMixin):
    def draw(self, canvas):
        self.draw_cube_frame(canvas, outline_color='black', width=2, fill='')

    def draw_rubber(self, canvas):
        return self.draw_cube_frame(canvas, outline_color='black', width=1, fill='')
