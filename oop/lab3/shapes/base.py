from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    @abstractmethod
    def draw(self, canvas): pass

    @abstractmethod
    def draw_rubber(self, canvas): pass