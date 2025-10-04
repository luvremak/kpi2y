import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
from typing import List, Optional


class Shape(ABC):
    def __init__(self):
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None
        self.end_x: Optional[int] = None
        self.end_y: Optional[int] = None
    
    @abstractmethod
    def draw(self, canvas: tk.Canvas) -> None:
        pass
    
    @abstractmethod
    def draw_rubber(self, canvas: tk.Canvas) -> None:
        pass
    
    def set_coords(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.start_x, self.start_y = x1, y1
        self.end_x, self.end_y = x2, y2


class PointShape(Shape):
    def draw(self, canvas: tk.Canvas) -> None:
        if self.start_x is not None and self.start_y is not None:
            r = 3
            canvas.create_oval(
                self.start_x - r, self.start_y - r,
                self.start_x + r, self.start_y + r,
                fill='black', outline='black'
            )
    
    def draw_rubber(self, canvas: tk.Canvas) -> None:
        if self.end_x is not None and self.end_y is not None:
            r = 3
            canvas.create_oval(
                self.end_x - r, self.end_y - r,
                self.end_x + r, self.end_y + r,
                outline='black', dash=(2, 2)
            )


class LineShape(Shape):
    def draw(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            canvas.create_line(
                self.start_x, self.start_y,
                self.end_x, self.end_y,
                fill='black', width=2
            )
    
    def draw_rubber(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            canvas.create_line(
                self.start_x, self.start_y,
                self.end_x, self.end_y,
                fill='black', dash=(4, 4)
            )


class RectShape(Shape):
    def draw(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            canvas.create_rectangle(
                self.start_x, self.start_y,
                self.end_x, self.end_y,
                outline='black', fill='#00FF00', width=2
            )
    
    def draw_rubber(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            canvas.create_rectangle(
                self.start_x, self.start_y,
                self.end_x, self.end_y,
                outline='black', dash=(4, 4)
            )


class EllipseShape(Shape):
    def draw(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            x1 = 2 * self.start_x - self.end_x
            y1 = 2 * self.start_y - self.end_y
            canvas.create_oval(
                x1, y1, self.end_x, self.end_y,
                outline='black', fill='white', width=2
            )
    
    def draw_rubber(self, canvas: tk.Canvas) -> None:
        if all([self.start_x, self.start_y, self.end_x, self.end_y]):
            x1 = 2 * self.start_x - self.end_x
            y1 = 2 * self.start_y - self.end_y
            canvas.create_oval(
                x1, y1, self.end_x, self.end_y,
                outline='black', dash=(4, 4)
            )


class Editor(ABC):
    def __init__(self):
        self.is_drawing = False
        self.current_shape: Optional[Shape] = None
    
    @abstractmethod
    def on_mouse_down(self, x: int, y: int) -> None:
        pass
    
    @abstractmethod
    def on_mouse_move(self, x: int, y: int) -> None:
        pass
    
    @abstractmethod
    def on_mouse_up(self, x: int, y: int) -> Shape:
        pass


class PointEditor(Editor):
    def on_mouse_down(self, x: int, y: int) -> None:
        self.current_shape = PointShape()
        self.current_shape.start_x = x
        self.current_shape.start_y = y
        self.is_drawing = True
    
    def on_mouse_move(self, x: int, y: int) -> None:
        if self.is_drawing and self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
    
    def on_mouse_up(self, x: int, y: int) -> Shape:
        if self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
            self.is_drawing = False
            return self.current_shape
        return None


class LineEditor(Editor):
    def on_mouse_down(self, x: int, y: int) -> None:
        self.current_shape = LineShape()
        self.current_shape.start_x = x
        self.current_shape.start_y = y
        self.is_drawing = True
    
    def on_mouse_move(self, x: int, y: int) -> None:
        if self.is_drawing and self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
    
    def on_mouse_up(self, x: int, y: int) -> Shape:
        if self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
            self.is_drawing = False
            return self.current_shape
        return None


class RectEditor(Editor):
    def on_mouse_down(self, x: int, y: int) -> None:
        self.current_shape = RectShape()
        self.current_shape.start_x = x
        self.current_shape.start_y = y
        self.is_drawing = True
    
    def on_mouse_move(self, x: int, y: int) -> None:
        if self.is_drawing and self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
    
    def on_mouse_up(self, x: int, y: int) -> Shape:
        if self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
            self.is_drawing = False
            return self.current_shape
        return None


class EllipseEditor(Editor):
    def on_mouse_down(self, x: int, y: int) -> None:
        self.current_shape = EllipseShape()
        self.current_shape.start_x = x
        self.current_shape.start_y = y
        self.is_drawing = True
    
    def on_mouse_move(self, x: int, y: int) -> None:
        if self.is_drawing and self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
    
    def on_mouse_up(self, x: int, y: int) -> Shape:
        if self.current_shape:
            self.current_shape.end_x = x
            self.current_shape.end_y = y
            self.is_drawing = False
            return self.current_shape
        return None


class ShapeEditorApp:
    MAX_SHAPES = 111
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lab2 - Графічний редактор")
        self.root.geometry("900x700")
        
        self.shapes: List[Optional[Shape]] = [None] * self.MAX_SHAPES
        self.shape_count = 0
        self.current_editor: Optional[Editor] = None
        self.current_mode = "Без режиму"
        
        self._create_menu()
        self._create_canvas()
        self._bind_events()
        self._update_title()
    
    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        objects_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)
        objects_menu.add_command(label="Точка", command=self._set_point_mode)
        objects_menu.add_command(label="Лінія", command=self._set_line_mode)
        objects_menu.add_command(label="Прямокутник", command=self._set_rect_mode)
        objects_menu.add_command(label="Еліпс", command=self._set_ellipse_mode)
        objects_menu.add_separator()
        objects_menu.add_command(label="Очистити все", command=self._clear_all)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
    
    def _create_canvas(self) -> None:
        self.canvas = tk.Canvas(self.root, width=900, height=700, bg='white', cursor='crosshair')
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def _bind_events(self) -> None:
        self.canvas.bind("<Button-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
    
    def _update_title(self) -> None:
        title = f"Lab2 - {self.current_mode} | Фігур: {self.shape_count}/{self.MAX_SHAPES}"
        self.root.title(title)
    
    def _set_point_mode(self) -> None:
        self.current_editor = PointEditor()
        self.current_mode = "Режим введення точок"
        self._update_title()
    
    def _set_line_mode(self) -> None:
        self.current_editor = LineEditor()
        self.current_mode = "Режим введення ліній"
        self._update_title()
    
    def _set_rect_mode(self) -> None:
        self.current_editor = RectEditor()
        self.current_mode = "Режим введення прямокутників"
        self._update_title()
    
    def _set_ellipse_mode(self) -> None:
        self.current_editor = EllipseEditor()
        self.current_mode = "Режим введення еліпсів"
        self._update_title()
    
    def _on_mouse_down(self, event) -> None:
        if self.current_editor and self.shape_count < self.MAX_SHAPES:
            self.current_editor.on_mouse_down(event.x, event.y)
    
    def _on_mouse_move(self, event) -> None:
        if self.current_editor and self.current_editor.is_drawing:
            self.current_editor.on_mouse_move(event.x, event.y)
            self._redraw()
    
    def _on_mouse_up(self, event) -> None:
        if self.current_editor and self.current_editor.is_drawing:
            new_shape = self.current_editor.on_mouse_up(event.x, event.y)
            if new_shape and self.shape_count < self.MAX_SHAPES:
                self.shapes[self.shape_count] = new_shape
                self.shape_count += 1
                self._update_title()
                self._redraw()
            elif self.shape_count >= self.MAX_SHAPES:
                messagebox.showwarning("Увага", f"Досягнуто максимум ({self.MAX_SHAPES} фігур)")
    
    def _redraw(self) -> None:
        self.canvas.delete("all")
        
        for i in range(self.shape_count):
            if self.shapes[i]:
                self.shapes[i].draw(self.canvas)
        
        if self.current_editor and self.current_editor.is_drawing:
            if self.current_editor.current_shape:
                self.current_editor.current_shape.draw_rubber(self.canvas)
    
    def _clear_all(self) -> None:
        if messagebox.askyesno("Підтвердження", "Очистити всі фігури?"):
            self.shapes = [None] * self.MAX_SHAPES
            self.shape_count = 0
            self._update_title()
            self._redraw()
    
    def _show_about(self) -> None:
        about_text = """Лабораторна робота №2
Графічний редактор геометричних фігур

Студентка: Крошка Дар'я
Група: ІМ-44, Номер: 11

Параметри (Ж=11):
• Статичний масив: 111 елементів
• Гумовий слід: пунктирна чорна лінія
• Прямокутник: світло-зелене заповнення
• Еліпс: введення від центру, біле заповнення
• Позначка режиму: в заголовку вікна

Реалізовано:
✓ Інкапсуляція
✓ Успадкування
✓ Поліморфізм"""
        messagebox.showinfo("Про програму", about_text)


def main():
    root = tk.Tk()
    app = ShapeEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()