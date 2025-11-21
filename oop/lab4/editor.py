import tkinter as tk
from tkinter import Menu
from .shapes.shape_factory import ShapeFactory
from .utils.constants import MAX_SHAPES, SHAPE_NAMES


class MyEditor:
    MAX_SHAPES = MAX_SHAPES

    def __init__(self, root):
        self.root = root
        self.root.title("MyEditor - Графічний редактор")
        self.root.geometry("1000x700")

        self.shapes = []
        self.current_shape = None
        self.shape_type = 'point'
        self.drawing = False

        self.start_x = self.start_y = 0

        self.rubber_ids = []

        self.create_menu()
        self.create_toolbar()

        self.canvas = tk.Canvas(root, bg='white', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

        self.info_label = tk.Label(root, text=f"Фігур: 0/{self.MAX_SHAPES} | Тип: {SHAPE_NAMES[self.shape_type]}",
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        shape_menu = Menu(menubar, tearoff=0, postcommand=self.on_init_menu_popup)
        menubar.add_cascade(label="Фігури", menu=shape_menu)

        self.menu_items = {}
        shapes = [
            ('Точка', 'point'),
            ('Лінія', 'line'),
            ('Прямокутник', 'rectangle'),
            ('Еліпс', 'ellipse'),
            ('Лінія з кружечками', 'line_circles'),
            ('Каркас куба', 'cube')
        ]
        for label, shape_type in shapes:
            # add_command returns None, so store just for reference
            shape_menu.add_command(label=label, command=lambda st=shape_type: self.set_shape_type(st))

        action_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Дії", menu=action_menu)
        action_menu.add_command(label="Очистити все", command=self.clear_all)
        action_menu.add_separator()
        action_menu.add_command(label="Вихід", command=self.root.quit)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ('Точка', 'point', '●'),
            ('Лінія', 'line', '╱'),
            ('Прямокутник', 'rectangle', '▭'),
            ('Еліпс', 'ellipse', '○'),
            ('Лінія+○', 'line_circles', '●—●'),
            ('Куб', 'cube', '▢')
        ]
        self.toolbar_buttons = {}
        for label, shape_type, symbol in buttons:
            btn = tk.Button(toolbar, text=f"{symbol}\n{label}",
                            command=lambda st=shape_type: self.set_shape_type(st),
                            width=8, height=2, relief=tk.RAISED)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.toolbar_buttons[shape_type] = btn

        self.toolbar_buttons['point'].config(relief=tk.SUNKEN, bg='lightblue')

    def on_init_menu_popup(self):
        pass

    def set_shape_type(self, shape_type):
        self.shape_type = shape_type
        for btn_type, btn in self.toolbar_buttons.items():
            if btn_type == shape_type:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        self.update_info()

    def on_mouse_down(self, event):
        if len(self.shapes) >= self.MAX_SHAPES:
            self.info_label.config(text=f"Досягнуто максимум фігур: {self.MAX_SHAPES}")
            return

        self.start_x, self.start_y = event.x, event.y

        if self.shape_type == 'point':
            shape = ShapeFactory.create(self.shape_type)
            shape.set_coords(event.x, event.y, event.x, event.y)
            self.shapes.append(shape)
            self.redraw()
            return

        self.drawing = True
        self.current_shape = ShapeFactory.create(self.shape_type)
        self.current_shape.set_coords(self.start_x, self.start_y, self.start_x, self.start_y)

        self._update_rubber(event.x, event.y)

    def on_mouse_move(self, event):
        if not self.drawing or self.shape_type == 'point':
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
        ids = self.current_shape.draw_rubber(self.canvas)

        if ids is None:
            ids = []
        elif not isinstance(ids, (list, tuple)):
            ids = [ids]
        self.rubber_ids.extend(ids)

    def on_mouse_up(self, event):
        if not self.drawing or self.shape_type == 'point':
            return

        if self.current_shape is None:
            self.drawing = False
            return

        self.current_shape.set_coords(self.start_x, self.start_y, event.x, event.y)

        self.shapes.append(self.current_shape)
        self.current_shape = None


        for _id in self.rubber_ids:
            try:
                self.canvas.delete(_id)
            except Exception:
                pass
        self.rubber_ids.clear()

        self.redraw()
        self.drawing = False

    def redraw(self):
        self.canvas.delete('all')
        for shape in self.shapes:
            shape.draw(self.canvas)
        self.update_info()

    def update_info(self):
        shape_name = SHAPE_NAMES.get(self.shape_type, 'Unknown')
        self.info_label.config(text=f"Фігур: {len(self.shapes)}/{self.MAX_SHAPES} | Тип: {shape_name}")

    def clear_all(self):
        self.shapes.clear()
        self.redraw()


editor = None


def main():
    global editor
    root = tk.Tk()
    editor = MyEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
