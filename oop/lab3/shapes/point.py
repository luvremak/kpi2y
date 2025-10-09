from .base import Shape

class Point(Shape):
    def draw(self, canvas):
        r = 3
        canvas.create_oval(self.x1 - r, self.y1 - r, self.x1 + r, self.y1 + r,
                           fill='black', outline='black')

    def draw_rubber(self, canvas):
        r = 3
        canvas.create_oval(self.x1 - r, self.y1 - r, self.x1 + r, self.y1 + r,
                           outline='black')
