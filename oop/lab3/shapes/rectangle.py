from .base import Shape

class Rectangle(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                outline='black', fill='yellow', width=2)

    def draw_rubber(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                outline='black', width=1)
