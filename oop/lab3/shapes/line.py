from .base import Shape

class Line(Shape):
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='black', width=2)

    def draw_rubber(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='black', width=1)
