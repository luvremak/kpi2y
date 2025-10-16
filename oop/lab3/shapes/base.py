from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1
        self.temp_id = None  

    def update(self, x2, y2):
        self.x2 = x2
        self.y2 = y2

    def show_rubber(self, canvas):
        if self.temp_id:
            canvas.delete(self.temp_id)
        self.temp_id = self.draw_rubber(canvas)

    def finalize(self, canvas):
        if self.temp_id:
            canvas.delete(self.temp_id)
        self.draw(canvas)

    @abstractmethod
    def draw(self, canvas): ...

    @abstractmethod
    def draw_rubber(self, canvas): ...
