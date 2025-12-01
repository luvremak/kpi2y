import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import pyperclip

class Object2Application:
    def __init__(self, root, n, min_val, max_val):
        self.root = root
        self.root.title("Object2 - Генерація вектора")
        self.root.geometry("800x600")
        
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        self.vector = None
        
        self.generate_vector()
        
        self.create_widgets()
        
        self.copy_to_clipboard()
        
    def generate_vector(self):
        self.vector = np.random.uniform(self.min_val, self.max_val, self.n)
        
    def create_widgets(self):
        title = tk.Label(self.root, text=f"Згенерований вектор ({self.n} елементів)", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        info = tk.Label(self.root, 
                       text=f"Діапазон: [{self.min_val}, {self.max_val}]",
                       font=("Arial", 10))
        info.pack(pady=5)
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.text_widget = tk.Text(frame, wrap=tk.NONE, font=("Courier", 10),
                                   yscrollcommand=scrollbar_y.set,
                                   xscrollcommand=scrollbar_x.set)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=self.text_widget.yview)
        scrollbar_x.config(command=self.text_widget.xview)
        
        self.display_vector()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        btn_copy = tk.Button(btn_frame, text="Копіювати в буфер обміну", 
                            command=self.copy_to_clipboard,
                            font=("Arial", 11), bg="#4CAF50", fg="white",
                            padx=15, pady=8)
        btn_copy.pack(side=tk.LEFT, padx=5)
        
        btn_close = tk.Button(btn_frame, text="Закрити", 
                             command=self.root.destroy,
                             font=("Arial", 11), bg="#f44336", fg="white",
                             padx=15, pady=8)
        btn_close.pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_label = tk.Label(self.root, text="Дані скопійовано в буфер обміну", 
                                     font=("Arial", 9), fg="green")
        self.status_label.pack(pady=5)
        
    def display_vector(self):
        self.text_widget.delete(1.0, tk.END)
        
        cols = min(5, max(1, self.n // 10))  
        if self.n <= 20:
            cols = 2
        elif self.n <= 50:
            cols = 3
        elif self.n <= 100:
            cols = 4
        else:
            cols = 5
        
        header = ""
        for col in range(cols):
            header += "Індекс".ljust(10) + "Значення".ljust(20)
        self.text_widget.insert(tk.END, header + "\n")
        self.text_widget.insert(tk.END, "=" * (cols * 30) + "\n\n")
        
        rows = (self.n + cols - 1) // cols 
        
        for row in range(rows):
            line = ""
            for col in range(cols):
                idx = row + col * rows
                if idx < self.n:
                    line += f"{idx}".ljust(10) + f"{self.vector[idx]:.6f}".ljust(20)
            self.text_widget.insert(tk.END, line + "\n")
            
    def copy_to_clipboard(self):
        try:
            text_data = "\n".join([f"{val:.10f}" for val in self.vector])
            
            pyperclip.copy(text_data)
            
            self.status_label.config(text="Дані успішно скопійовано в буфер обміну", fg="green")
            messagebox.showinfo("Успіх", f"Вектор з {self.n} елементів скопійовано в буфер обміну.")
        except Exception as e:
            self.status_label.config(text=f"Помилка копіювання: {e}", fg="red")
            messagebox.showerror("Помилка", f"Не вдалося скопіювати в буфер обміну:\n{e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Помилка", "Програма повинна запускатися з параметрами: n, Min, Max")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        min_val = float(sys.argv[2])
        max_val = float(sys.argv[3])
        
        root = tk.Tk()
        app = Object2Application(root, n, min_val, max_val)
        root.mainloop()
    except ValueError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Помилка", "Невірний формат параметрів")
        sys.exit(1)