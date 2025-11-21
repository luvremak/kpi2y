from .base import Shape


class PointShape(Shape):
    def draw(self, canvas):
        canvas.create_oval(
            self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2,
            fill='black', outline='black'
        )

    def draw_rubber(self, canvas):
        return canvas.create_oval(
            self.x1 - 2, self.y1 - 2, self.x1 + 2, self.y1 + 2,
            outline='gray', fill=''
        )


class LineShape(Shape):
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='black', width=2)

    def draw_rubber(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='gray', dash=(4, 4), width=2)


class RectShape(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='black', fill='yellow', width=2)

    def draw_rubber(self, canvas):
        return canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline='gray', fill='', dash=(4, 4), width=2)


class EllipseShape(Shape):
    def draw(self, canvas):
        cx, cy = self.x1, self.y1
        rx = abs(self.x2 - self.x1)
        ry = abs(self.y2 - self.y1)
        canvas.create_oval(cx - rx, cy - ry, cx + rx, cy + ry, outline='black', fill='', width=2)

    def draw_rubber(self, canvas):
        cx, cy = self.x1, self.y1
        rx = abs(self.x2 - self.x1)
        ry = abs(self.y2 - self.y1)
        return canvas.create_oval(cx - rx, cy - ry, cx + rx, cy + ry, outline='gray', fill='', dash=(4, 4), width=2)
