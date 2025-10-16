from .base import Shape

class Ellipse(Shape):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)  
        self.cx = cx
        self.cy = cy

    def update(self, x2, y2):
        rx = abs(x2 - self.cx)
        ry = abs(y2 - self.cy)
        self.x1 = self.cx - rx
        self.y1 = self.cy - ry
        self.x2 = self.cx + rx
        self.y2 = self.cy + ry

    def draw(self, canvas):
        return canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline='black', fill='', width=2
        )

    def draw_rubber(self, canvas):
        return canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline='black', width=1
        )
