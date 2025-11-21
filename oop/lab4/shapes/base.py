from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @abstractmethod
    def draw(self, canvas):
        """Draw the permanent shape on canvas (no return)."""
        pass

    def draw_rubber(self, canvas):
        """
        Draw temporary preview shapes on canvas and return the created canvas ids.
        Default implementation returns empty list (no rubber).
        Subclasses should return a list of ids or a single id.
        """
        return []

    def set_coords(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
