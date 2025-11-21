import tkinter as tk


class CanvasManager:
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def clear(self):
        self.shapes.clear()
        self.canvas.delete('all')

    def redraw(self):
        self.canvas.delete('all')
        for shape in self.shapes:
            shape.draw(self.canvas)

    def get_count(self):
        return len(self.shapes)

    def is_full(self, max_shapes):
        return self.get_count() >= max_shapes