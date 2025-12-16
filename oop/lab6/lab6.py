import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import socket
import json
import time

class Lab6App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab6 - Головне вікно")
        self.root.geometry("300x300+100+100")
        
        # Обробка закриття вікна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Елементи інтерфейсу
        tk.Label(root, text="Кількість (N):").pack(pady=5)
        self.entry_n = tk.Entry(root)
        self.entry_n.insert(0, "10")
        self.entry_n.pack(pady=5)

        tk.Label(root, text="Min значення:").pack(pady=5)
        self.entry_min = tk.Entry(root)
        self.entry_min.insert(0, "0.0")
        self.entry_min.pack(pady=5)

        tk.Label(root, text="Max значення:").pack(pady=5)
        self.entry_max = tk.Entry(root)
        self.entry_max.insert(0, "100.0")
        self.entry_max.pack(pady=5)

        btn = tk.Button(root, text="Виконати / Оновити", command=self.send_update, bg="#4CAF50", fg="white")
        btn.pack(pady=20, fill=tk.X, padx=20)

        # Зберігаємо процеси
        self.proc_obj2 = None
        self.proc_obj3 = None
        
        # Автоматичний запуск компонентів при старті
        self.launch_components()

    def launch_components(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Запускаємо Object2
        path_obj2 = os.path.join(current_dir, "Object2.py")
        self.proc_obj2 = subprocess.Popen([sys.executable, path_obj2])
        
        # Запускаємо Object3
        path_obj3 = os.path.join(current_dir, "Object3.py")
        self.proc_obj3 = subprocess.Popen([sys.executable, path_obj3])
        
        print("Компоненти запущено. Очікування ініціалізації...")
        # Даємо час програмам запуститися і відкрити порти
        time.sleep(1.5) 

    def send_update(self):
        try:
            n = int(self.entry_n.get())
            min_val = float(self.entry_min.get())
            max_val = float(self.entry_max.get())

            if min_val >= max_val or n <= 0:
                messagebox.showerror("Помилка", "Перевірте вхідні дані!")
                return

            data = {"n": n, "min": min_val, "max": max_val}
            
            # ВІДПРАВКА ДАНИХ НА OBJECT2 (Порт 65432)
            # Lab6 спілкується лише з Object2, а Object2 вже передасть далі на Object3
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('127.0.0.1', 65432))
                    s.sendall(json.dumps(data).encode('utf-8'))
                    print(f"Дані відправлено в Object2: {data}")
            except ConnectionRefusedError:
                messagebox.showerror("Помилка зв'язку", "Object2 ще не готовий або закритий.")

        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні числа.")

    def on_close(self):
        # Примусове завершення дочірніх процесів
        if self.proc_obj2:
            self.proc_obj2.terminate()
        if self.proc_obj3:
            self.proc_obj3.terminate()
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Lab6App(root)
    root.mainloop()