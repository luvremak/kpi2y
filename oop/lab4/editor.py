import tkinter as tk
from tkinter import Menu
from shapes.simple_shapes import PointShape, LineShape, RectShape, EllipseShape
from shapes.complex_shapes import LineWithCircles, CubeFrame
from utils.constants import MAX_SHAPES, SHAPE_NAMES

class MyEditor:
    MAX_SHAPES = 112
    
    def __init__(self, root):
        self.root = root
        self.root.title("MyEditor - Графічний редактор")
        self.root.geometry("1000x700")

        self.shapes = []
        self.current_shape = None
        self.shape_type = 'point'
        self.drawing = False
        self.start_x = self.start_y = 0
        self.rubber_line = None

        self.create_menu()

        self.create_toolbar()

        self.canvas = tk.Canvas(root, bg='white', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

        self.info_label = tk.Label(root, text=f"Фігур: 0/{self.MAX_SHAPES} | Тип: Точка",
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
            self.menu_items[shape_type] = shape_menu.add_command(
                label=label,
                command=lambda st=shape_type: self.set_shape_type(st)
            )
        
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
        shape_names = {
            'point': 'Точка',
            'line': 'Лінія',
            'rectangle': 'Прямокутник',
            'ellipse': 'Еліпс',
            'line_circles': 'Лінія з кружечками',
            'cube': 'Каркас куба'
        }
        pass
    
    def set_shape_type(self, shape_type):
        self.shape_type = shape_type
        
        for btn_type, btn in self.toolbar_buttons.items():
            if btn_type == shape_type:
                btn.config(relief=tk.SUNKEN, bg='lightblue')
            else:
                btn.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        shape_names = {
            'point': 'Точка',
            'line': 'Лінія',
            'rectangle': 'Прямокутник',
            'ellipse': 'Еліпс',
            'line_circles': 'Лінія з кружечками',
            'cube': 'Каркас куба'
        }
        self.update_info(shape_names[shape_type])
    
    def on_mouse_down(self, event):
        if len(self.shapes) >= self.MAX_SHAPES:
            self.info_label.config(text=f"Досягнуто максимум фігур: {self.MAX_SHAPES}")
            return
        
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y

        if self.shape_type == 'point':
            shape = PointShape()
            shape.set_coords(event.x, event.y, event.x, event.y)
            self.shapes.append(shape)
            self.redraw()
            self.drawing = False
    
    def on_mouse_move(self, event):
        if not self.drawing or self.shape_type == 'point':
            return

        if self.rubber_line:
            self.canvas.delete(self.rubber_line)
        
        if self.shape_type in ['line', 'line_circles']:
            self.rubber_line = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill='black', width=2
            )
        elif self.shape_type == 'rectangle' or self.shape_type == 'cube':
            self.rubber_line = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='black', width=2
            )
        elif self.shape_type == 'ellipse':
            rx = abs(event.x - self.start_x)
            ry = abs(event.y - self.start_y)
            self.rubber_line = self.canvas.create_oval(
                self.start_x-rx, self.start_y-ry,
                self.start_x+rx, self.start_y+ry,
                outline='black', width=2
            )
    
    def on_mouse_up(self, event):
        if not self.drawing or self.shape_type == 'point':
            return

        if self.rubber_line:
            self.canvas.delete(self.rubber_line)
            self.rubber_line = None
        
        shape = None
        if self.shape_type == 'line':
            shape = LineShape()
            shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        elif self.shape_type == 'rectangle':
            shape = RectShape()
            shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        elif self.shape_type == 'ellipse':
            shape = EllipseShape()
            shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        elif self.shape_type == 'line_circles':
            shape = LineWithCircles()
            shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        elif self.shape_type == 'cube':
            shape = CubeFrame()
            shape.set_coords(self.start_x, self.start_y, event.x, event.y)
        
        if shape:
            self.shapes.append(shape)
            self.redraw()
        
        self.drawing = False
    
    def redraw(self):
        self.canvas.delete('all')
        for shape in self.shapes:
            shape.draw(self.canvas)
        self.update_info()
    
    def update_info(self, shape_name=None):
        if shape_name is None:
            shape_names = {
                'point': 'Точка',
                'line': 'Лінія',
                'rectangle': 'Прямокутник',
                'ellipse': 'Еліпс',
                'line_circles': 'Лінія з кружечками',
                'cube': 'Каркас куба'
            }
            shape_name = shape_names[self.shape_type]
        
        self.info_label.config(
            text=f"Фігур: {len(self.shapes)}/{self.MAX_SHAPES} | Тип: {shape_name}"
        )
    
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