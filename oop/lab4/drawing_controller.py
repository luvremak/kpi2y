# drawing_controller.py
import tkinter as tk
from .shapes.shape_factory import ShapeFactory


class DrawingController:

    def __init__(self, canvas: tk.Canvas, shape_manager, editor):
        self.canvas = canvas
        self.shape_manager = shape_manager
        self.editor = editor  

        self.drawing = False
        self.current_shape = None
        self.start_x = 0
        self.start_y = 0
        self.rubber_ids = []

    def on_mouse_down(self, event):
        if len(self.shape_manager.shapes) >= self.shape_manager.MAX_SHAPES:
            self.editor.info_label.config(text=f"Досягнуто максимум фігур: {self.shape_manager.MAX_SHAPES}")
            return

        self.start_x, self.start_y = event.x, event.y

        if self.editor.shape_type == 'point':
            shape = ShapeFactory.create(self.editor.shape_type)
            shape.set_coords(event.x, event.y, event.x, event.y)
            self.shape_manager.add_shape(shape)
            self.editor.redraw()
            return

        self.drawing = True
        self.current_shape = ShapeFactory.create(self.editor.shape_type)
        self.current_shape.set_coords(self.start_x, self.start_y, self.start_x, self.start_y)
        self._update_rubber(event.x, event.y)

    def on_mouse_move(self, event):
        if not self.drawing or self.editor.shape_type == 'point':
            return
        self._update_rubber(event.x, event.y)

    def _update_rubber(self, x, y):
        for _id in self.rubber_ids:
            try:
                self.canvas.delete(_id)
            except Exception:
                pass
        self.rubber_ids.clear()

        if self.current_shape is None:
            return

        self.current_shape.set_coords(self.start_x, self.start_y, x, y)
        ids = None
        try:
            ids = self.current_shape.draw_rubber(self.canvas)
        except Exception:
            ids = None

        if ids is None:
            ids = []
        elif not isinstance(ids, (list, tuple)):
            ids = [ids]
        self.rubber_ids.extend(ids)

    def on_mouse_up(self, event):
        if not self.drawing or self.editor.shape_type == 'point':
            return

        if self.current_shape is None:
            self.drawing = False
            return

        self.current_shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        added = self.shape_manager.add_shape(self.current_shape)
        self.current_shape = None

        for _id in self.rubber_ids:
            try:
                self.canvas.delete(_id)
            except Exception:
                pass
        self.rubber_ids.clear()

        self.editor.redraw()
        self.drawing = False
