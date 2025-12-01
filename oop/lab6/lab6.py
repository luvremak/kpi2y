import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import sys
import time

class Lab6Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab6 - Головна програма")
        self.root.geometry("400x300")
        
        self.n = None
        self.min_val = None
        self.max_val = None
        
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self.root, text="Лабораторна робота 6", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        info = tk.Label(self.root, text="Введіть параметри для генерації вектора",
                       font=("Arial", 10))
        info.pack(pady=10)
        
        btn_input = tk.Button(self.root, text="Ввести параметри", 
                             command=self.input_parameters,
                             font=("Arial", 12), bg="#4CAF50", fg="white",
                             padx=20, pady=10)
        btn_input.pack(pady=10)
        
        self.btn_object2 = tk.Button(self.root, text="Запустити Object2 (Генерація)", 
                                     command=self.run_object2,
                                     font=("Arial", 12), bg="#2196F3", fg="white",
                                     padx=20, pady=10, state=tk.DISABLED)
        self.btn_object2.pack(pady=5)
        
        self.btn_object3 = tk.Button(self.root, text="Запустити Object3 (Графік)", 
                                     command=self.run_object3,
                                     font=("Arial", 12), bg="#FF9800", fg="white",
                                     padx=20, pady=10, state=tk.DISABLED)
        self.btn_object3.pack(pady=5)
        
        self.status_label = tk.Label(self.root, text="Статус: Очікування введення", 
                                     font=("Arial", 9), fg="gray")
        self.status_label.pack(pady=20)
        
    def input_parameters(self):
        n = simpledialog.askinteger("Введення", "Введіть кількість елементів (n):",
                                   minvalue=1, maxvalue=1000)
        if n is None:
            return
            
        min_val = simpledialog.askfloat("Введення", "Введіть мінімальне значення (Min):")
        if min_val is None:
            return
            
        max_val = simpledialog.askfloat("Введення", "Введіть максимальне значення (Max):")
        if max_val is None:
            return
            
        if min_val >= max_val:
            messagebox.showerror("Помилка", "Min повинно бути менше Max!")
            return
            
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        
        self.btn_object2.config(state=tk.NORMAL)
        self.btn_object3.config(state=tk.NORMAL)
        
        self.status_label.config(text=f"Параметри: n={n}, Min={min_val}, Max={max_val}")
        messagebox.showinfo("Успіх", f"Параметри збережено:\nn = {n}\nMin = {min_val}\nMax = {max_val}")
        
    def run_object2(self):
        if self.n is None:
            messagebox.showwarning("Увага", "Спочатку введіть параметри!")
            return
            
        try:
            subprocess.Popen([sys.executable, "object2.py", 
                            str(self.n), str(self.min_val), str(self.max_val)])
            self.status_label.config(text="Object2 запущено")
            messagebox.showinfo("Інформація", "Object2 запущено. Дані будуть згенеровані та скопійовані в буфер обміну.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося запустити Object2:\n{e}")
            
    def run_object3(self):
        try:
            subprocess.Popen([sys.executable, "object3.py"])
            self.status_label.config(text="Object3 запущено")
            messagebox.showinfo("Інформація", "Object3 запущено. Графік буде побудовано з даних буфера обміну.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося запустити Object3:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Lab6Application(root)
    root.mainloop()