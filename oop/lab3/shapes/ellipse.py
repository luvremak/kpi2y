from .base import Shape

class Ellipse(Shape):
    def __init__(self, cx, cy, x2, y2):
        rx, ry = abs(x2 - cx), abs(y2 - cy)
        super().__init__(cx - rx, cy - ry, cx + rx, cy + ry)
        self.cx, self.cy = cx, cy

    def draw(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           outline='black', fill='', width=2)

    def draw_rubber(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           outline='black', width=1)
