import tkinter as tk
from tkinter import ttk, messagebox
from shapes import Point, Line, Rectangle, Ellipse, Star
from utils import create_tooltip


class GraphicEditor:
    SHAPES_CONFIG = {
        'point': {'name': 'Крапка', 'icon': '•', 'class': Point},
        'line': {'name': 'Лінія', 'icon': '/', 'class': Line},
        'rectangle': {'name': 'Прямокутник', 'icon': '▭', 'class': Rectangle},
        'ellipse': {'name': 'Еліпс', 'icon': '○', 'class': Ellipse},
        'star': {'name': 'Зірочка', 'icon': '★', 'class': Star}
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор Lab3")
        self.root.geometry("1000x700")
        
        self.shapes = []
        self.current_shape_type = 'point'
        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0
        self.rubber_id = None
        
        self.setup_menu()
        self.setup_toolbar()
        self.setup_canvas()
        self.setup_statusbar()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        
        self.objects_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Об'єкти", menu=self.objects_menu)
        
        self.shape_var = tk.StringVar(value=self.current_shape_type)
        
        for shape_key, config in self.SHAPES_CONFIG.items():
            self.objects_menu.add_radiobutton(
                label=f"{config['icon']} {config['name']}", 
                variable=self.shape_var,
                value=shape_key,
                command=lambda k=shape_key: self.set_shape_type(k)
            )
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self.show_about)
        
    def setup_toolbar(self):
        toolbar_frame = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        ttk.Label(toolbar_frame, text="Інструменти:", 
                  font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.toolbar_buttons = {}
        for shape_key, config in self.SHAPES_CONFIG.items():
            btn = ttk.Button(
                toolbar_frame,
                text=f"{config['icon']} {config['name']}",
                command=lambda k=shape_key: self.set_shape_type(k),
                width=15
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.toolbar_buttons[shape_key] = btn
            
            create_tooltip(btn, f"Обрати інструмент: {config['name']}")
        
        self.update_toolbar_selection()
        
    def setup_canvas(self):
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

    def setup_statusbar(self):
        statusbar = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(statusbar, text="Готово до роботи", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.shapes_count_label = ttk.Label(statusbar, text="Об'єктів: 0", anchor=tk.E)
        self.shapes_count_label.pack(side=tk.RIGHT, padx=5)
        
    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type
        self.shape_var.set(shape_type)
        self.update_toolbar_selection()
        config = self.SHAPES_CONFIG[shape_type]
        self.status_label.config(text=f"Обрано інструмент: {config['name']}")
        
    def update_toolbar_selection(self):
        for key, btn in self.toolbar_buttons.items():
            if key == self.current_shape_type:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])
                
    def on_mouse_down(self, event):
        self.is_drawing = True
        self.start_x = event.x
        self.start_y = event.y
        
    def on_mouse_move(self, event):
        if not self.is_drawing:
            return
        
        if self.rubber_id:
            self.canvas.delete(self.rubber_id)
        
        shape_class = self.SHAPES_CONFIG[self.current_shape_type]['class']
        
        if self.current_shape_type == 'ellipse':
            temp_shape = shape_class(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == 'point':
            temp_shape = shape_class(self.start_x, self.start_y, self.start_x, self.start_y)
        else:
            temp_shape = shape_class(self.start_x, self.start_y, event.x, event.y)
        
        items_before = self.canvas.find_all()
        temp_shape.draw_rubber(self.canvas)
        items_after = self.canvas.find_all()
        
        new_items = [item for item in items_after if item not in items_before]
        self.rubber_id = new_items if new_items else None
        
    def on_mouse_up(self, event):
        if not self.is_drawing:
            return
        
        self.is_drawing = False
        
        if self.rubber_id:
            if isinstance(self.rubber_id, list):
                for item in self.rubber_id:
                    self.canvas.delete(item)
            else:
                self.canvas.delete(self.rubber_id)
            self.rubber_id = None
        
        shape_class = self.SHAPES_CONFIG[self.current_shape_type]['class']
        
        if self.current_shape_type == 'ellipse':
            shape = shape_class(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape_type == 'point':
            shape = shape_class(self.start_x, self.start_y, self.start_x, self.start_y)
        else:
            shape = shape_class(self.start_x, self.start_y, event.x, event.y)
        
        if len(self.shapes) < 112:
            self.shapes.append(shape)
            self.redraw_canvas()
            self.update_shapes_count()
        else:
            messagebox.showwarning("Обмеження", "Досягнуто максимальну кількість об'єктів (112)")
        
    def redraw_canvas(self):
        self.canvas.delete('all')
        for shape in self.shapes:
            shape.draw(self.canvas)
            
    def update_shapes_count(self):
        self.shapes_count_label.config(text=f"Об'єктів: {len(self.shapes)}/112")
        
    def clear_canvas(self):
        if messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете очистити полотно?"):
            self.shapes.clear()
            self.canvas.delete('all')
            self.update_shapes_count()
            self.status_label.config(text="Полотно очищено")
            
    def show_about(self):
        about_text = """Графічний редактор Lab3

Варіант завдання:

Тип масиву: Динамічний (Shape **pcshape)
Кількість елементів: 112

Гумовий слід: Суцільна чорна лінія

Прямокутник (увід): По двох протилежних кутах
Прямокутник (відображення): Чорний контур, жовте заповнення

Еліпс (увід): Від центру
Еліпс (відображення): Чорний контур без заповнення

Позначка поточного типу: В меню (OnInitMenuPopup)"""
        
        messagebox.showinfo("Про програму", about_text)
