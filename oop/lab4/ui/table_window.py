import tkinter as tk
from tkinter import ttk
from .utils.constants import SHAPE_NAMES


class TableWindow:

    def __init__(self, parent, editor):
        self.editor = editor
        self.window = tk.Toplevel(parent)
        self.window.title("Таблиця об'єктів")
        self.window.geometry("600x400")

        self.window.transient(parent)

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
        self._setup_callbacks()
        self.refresh_table()

    def _create_widgets(self):

        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('№', 'Тип', 'x1', 'y1', 'x2', 'y2')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')

        self.tree.heading('№', text='№')
        self.tree.heading('Тип', text='Тип фігури')
        self.tree.heading('x1', text='x1')
        self.tree.heading('y1', text='y1')
        self.tree.heading('x2', text='x2')
        self.tree.heading('y2', text='y2')

        self.tree.column('№', width=50, anchor='center')
        self.tree.column('Тип', width=180, anchor='w')
        self.tree.column('x1', width=80, anchor='center')
        self.tree.column('y1', width=80, anchor='center')
        self.tree.column('x2', width=80, anchor='center')
        self.tree.column('y2', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)

        button_frame = tk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.delete_button = tk.Button(button_frame, text="Видалити обраний", 
                                       command=self.delete_selected, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(button_frame, text="Оновити", 
                                        command=self.refresh_table)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        self.close_button = tk.Button(button_frame, text="Закрити", 
                                      command=self.close)
        self.close_button.pack(side=tk.RIGHT, padx=5)
        
        self.info_label = tk.Label(self.window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_callbacks(self):
        self.editor.add_shape_change_listener(self.on_shapes_changed)

    def on_shapes_changed(self):
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        shape_type_reverse_map = {
            'PointShape': 'Точка',
            'LineShape': 'Лінія',
            'RectShape': 'Прямокутник',
            'EllipseShape': 'Еліпс',
            'LineWithCircles': 'Лінія з кружечками',
            'CubeFrame': 'Каркас куба'
        }
        
        for i, shape in enumerate(self.editor.shapes, start=1):
            shape_class = shape.__class__.__name__
            shape_name = shape_type_reverse_map.get(shape_class, shape_class)
            
            values = (
                i,
                shape_name,
                int(shape.x1),
                int(shape.y1),
                int(shape.x2),
                int(shape.y2)
            )
            self.tree.insert('', tk.END, values=values, tags=(str(i-1),))
        
        count = len(self.editor.shapes)
        self.info_label.config(text=f"Всього фігур: {count} / {self.editor.MAX_SHAPES}")

    def on_row_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            tags = self.tree.item(item, 'tags')
            if tags:
                index = int(tags[0])
                self.editor.select_shape(index)
                self.delete_button.config(state=tk.NORMAL)
        else:
            self.editor.select_shape(-1)
            self.delete_button.config(state=tk.DISABLED)

    def delete_selected(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            tags = self.tree.item(item, 'tags')
            if tags:
                index = int(tags[0])
                self.editor.delete_shape(index)
                self.delete_button.config(state=tk.DISABLED)

    def close(self):
        self.editor.remove_shape_change_listener(self.on_shapes_changed)
        self.editor.select_shape(-1)
        self.window.destroy()