import tkinter as tk
from tkinter import ttk, messagebox
from shapes.factory import ShapeFactory
from utils import create_tooltip


class GraphicEditor:
    MAX_SHAPES = 112

    SHAPES_CONFIG = {
        'point': {'name': 'Крапка', 'icon': '•'},
        'line': {'name': 'Лінія', 'icon': '/'},
        'rectangle': {'name': 'Прямокутник', 'icon': '▭'},
        'ellipse': {'name': 'Еліпс', 'icon': '○'},
        'star': {'name': 'Зірочка', 'icon': '★'}
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор Lab3")
        self.root.geometry("1000x700")

        self.shapes = []
        self.current_shape_type = 'point'
        self.current_shape = None

        self.setup_menu()
        self.setup_toolbar()
        self.setup_canvas()
        self.setup_statusbar()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

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
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas = tk.Canvas(frame, bg='white', cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

    def setup_statusbar(self):
        bar = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = ttk.Label(bar, text="Готово до роботи", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.shapes_count_label = ttk.Label(bar, text="Об'єктів: 0", anchor=tk.E)
        self.shapes_count_label.pack(side=tk.RIGHT, padx=5)

    def set_shape_type(self, shape_type):
        self.current_shape_type = shape_type
        self.shape_var.set(shape_type)
        self.update_toolbar_selection()
        name = self.SHAPES_CONFIG[shape_type]['name']
        self.status_label.config(text=f"Обрано інструмент: {name}")

    def update_toolbar_selection(self):
        for key, btn in self.toolbar_buttons.items():
            if key == self.current_shape_type:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

    def on_mouse_down(self, event):
        self.current_shape = ShapeFactory.create_shape(self.current_shape_type, event.x, event.y)

    def on_mouse_move(self, event):
        getattr(self.current_shape, 'update', lambda x, y: None)(event.x, event.y)
        getattr(self.current_shape, 'show_rubber', lambda canvas: None)(self.canvas)

    def on_mouse_up(self, event):
        update_and_finalize = lambda shape: (
            shape.update(event.x, event.y),
            shape.finalize(self.canvas),
            self.shapes.append(shape),
            self.update_shapes_count()
        )
        update_and_finalize(self.current_shape) if self.current_shape and len(self.shapes) < self.MAX_SHAPES else \
            messagebox.showwarning("Обмеження", f"Досягнуто максимум — {self.MAX_SHAPES} об'єктів") if self.current_shape else None
        self.current_shape = None


    def update_shapes_count(self):
        self.shapes_count_label.config(text=f"Об'єктів: {len(self.shapes)}/{self.MAX_SHAPES}")

    def clear_canvas(self):
        if messagebox.askyesno("Підтвердження", "Очистити полотно?"):
            self.shapes.clear()
            self.canvas.delete('all')
            self.update_shapes_count()
            self.status_label.config(text="Полотно очищено")

    def show_about(self):
        about_text = """Графічний редактор Lab3

Варіант завдання:
Тип масиву: Динамічний (Shape **pcshape)
Кількість елементів: 112

Гумовий слід: суцільна чорна лінія
Прямокутник: чорний контур, жовте заповнення
Еліпс: чорний контур без заповнення, вводиться від центру
Позначка типу: у меню (OnInitMenuPopup)
"""
        messagebox.showinfo("Про програму", about_text)
