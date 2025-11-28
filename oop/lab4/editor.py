import tkinter as tk
from tkinter import Menu, filedialog, messagebox
from .shapes.shape_factory import ShapeFactory
from .utils.constants import MAX_SHAPES, SHAPE_NAMES
from .ui.table_window import TableWindow
import json


class MyEditor:
    _instance = None
    MAX_SHAPES = MAX_SHAPES

    def __new__(cls, root=None):
        if cls._instance is None:
            cls._instance = super(MyEditor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, root=None):
        if self._initialized:
            return
        
        if root is None:
            raise ValueError("Root window must be provided on first initialization")
        
        self._initialized = True
        self.root = root
        self.root.title("MyEditor - Графічний редактор")
        self.root.geometry("1000x700")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.shapes = []
        self.current_shape = None
        self.shape_type = 'point'
        self.drawing = False
        self.selected_index = None 

        self._shape_change_listeners = []
        self._selection_listeners = []

        self.start_x = self.start_y = 0
        self.rubber_ids = []

        self.table_window = None

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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Editor not initialized. Call MyEditor(root) first.")
        return cls._instance

    def add_shape_change_listener(self, callback):
        if callback not in self._shape_change_listeners:
            self._shape_change_listeners.append(callback)

    def remove_shape_change_listener(self, callback):
        if callback in self._shape_change_listeners:
            self._shape_change_listeners.remove(callback)

    def add_selection_listener(self, callback):
        if callback not in self._selection_listeners:
            self._selection_listeners.append(callback)

    def remove_selection_listener(self, callback):
        if callback in self._selection_listeners:
            self._selection_listeners.remove(callback)

    def _notify_shape_change(self):
        for callback in self._shape_change_listeners:
            callback()

    def _notify_selection_change(self, index):
        for callback in self._selection_listeners:
            callback(index)

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
            shape_menu.add_command(label=label, command=lambda st=shape_type: self.set_shape_type(st))

        action_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Дії", menu=action_menu)
        action_menu.add_command(label="Очистити все", command=self.clear_all)
        action_menu.add_separator()
        action_menu.add_command(label="Вихід", command=self.on_closing)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Зберегти...", command=self.save_to_file)
        file_menu.add_command(label="Завантажити...", command=self.load_from_file)

        window_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вікна", menu=window_menu)
        window_menu.add_command(label="Таблиця об'єктів", command=self.toggle_table_window)

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
            self._notify_shape_change()
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
        self._notify_shape_change()
        self.drawing = False

    def redraw(self):
        self.canvas.delete('all')
        for i, shape in enumerate(self.shapes):
            if i == self.selected_index:
                self._draw_shape_highlighted(shape)
            else:
                shape.draw(self.canvas)
        self.update_info()

    def _draw_shape_highlighted(self, shape):

        padding = 10
        x1, y1, x2, y2 = shape.x1, shape.y1, shape.x2, shape.y2
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        self.canvas.create_rectangle(
            min_x - padding, min_y - padding,
            max_x + padding, max_y + padding,
            outline='red', width=3, dash=(5, 5)
        )

        shape.draw(self.canvas)

    def update_info(self):
        shape_name = SHAPE_NAMES.get(self.shape_type, 'Unknown')
        self.info_label.config(text=f"Фігур: {len(self.shapes)}/{self.MAX_SHAPES} | Тип: {shape_name}")

    def clear_all(self):
        self.shapes.clear()
        self.selected_index = None
        self.redraw()
        self._notify_shape_change()

    def select_shape(self, index):
        if 0 <= index < len(self.shapes):
            self.selected_index = index
            self.redraw()
        else:
            self.selected_index = None
            self.redraw()

    def delete_shape(self, index):
        if 0 <= index < len(self.shapes):
            del self.shapes[index]
            self.selected_index = None
            self.redraw()
            self._notify_shape_change()

    def toggle_table_window(self):
        if self.table_window is None or not self.table_window.window.winfo_exists():
            self.table_window = TableWindow(self.root, self)
        else:
            self.table_window.close()
            self.table_window = None

    def save_to_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:
            return

        try:
            data = []
            for shape in self.shapes:
                shape_data = {
                    'type': shape.__class__.__name__,
                    'x1': shape.x1,
                    'y1': shape.y1,
                    'x2': shape.x2,
                    'y2': shape.y2
                }
                data.append(shape_data)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Успіх", f"Збережено {len(data)} фігур у файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{str(e)}")

    def load_from_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            shape_type_map = {
                'PointShape': 'point',
                'LineShape': 'line',
                'RectShape': 'rectangle',
                'EllipseShape': 'ellipse',
                'LineWithCircles': 'line_circles',
                'CubeFrame': 'cube'
            }

            self.shapes.clear()
            loaded_count = 0

            for shape_data in data:
                if len(self.shapes) >= self.MAX_SHAPES:
                    break

                shape_class = shape_data.get('type')
                shape_type = shape_type_map.get(shape_class)

                if shape_type:
                    shape = ShapeFactory.create(shape_type)
                    shape.set_coords(
                        shape_data['x1'],
                        shape_data['y1'],
                        shape_data['x2'],
                        shape_data['y2']
                    )
                    self.shapes.append(shape)
                    loaded_count += 1

            self.selected_index = None
            self.redraw()
            self._notify_shape_change()

            messagebox.showinfo("Успіх", f"Завантажено {loaded_count} фігур з файлу:\n{filename}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити файл:\n{str(e)}")

    def on_closing(self):
        if self.table_window is not None:
            try:
                self.table_window.close()
            except:
                pass
        self.root.quit()
        self.root.destroy()


def main():

    root = tk.Tk()
    editor = MyEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
