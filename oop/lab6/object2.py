import tkinter as tk
import random
import socket
import json
import threading
import queue

class Object2App:
    def __init__(self, root):
        self.root = root
        self.root.title("Object2 - Генератор (Port 65432)")
        self.root.geometry("400x300+410+100")

        self.label = tk.Label(root, text="Очікування даних від Lab6...", font=("Arial", 10))
        self.label.pack(pady=10)

        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Черга для передачі даних з потоку сокета в потік GUI
        self.gui_queue = queue.Queue()
        
        # Запуск перевірки черги
        self.root.after(100, self.process_queue)
        
        # Запуск сервера в окремому потоці
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

    def start_server(self):
        HOST = '127.0.0.1'
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Дозволяє швидко перезапускати порт
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    data_raw = conn.recv(1024)
                    if data_raw:
                        # Отримали параметри від Lab6
                        params = json.loads(data_raw.decode('utf-8'))
                        # Кладемо в чергу для обробки в GUI
                        self.gui_queue.put(params)

    def process_queue(self):
        try:
            while True:
                params = self.gui_queue.get_nowait()
                self.generate_and_update(params)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def generate_and_update(self, params):
        n = params['n']
        min_val = params['min']
        max_val = params['max']
        
        # Генерація
        data_list = [random.uniform(min_val, max_val) for _ in range(n)]
        
        # Оновлення таблиці
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        columns = 3
        for i, val in enumerate(data_list):
            row = i // columns
            col = i % columns
            lbl = tk.Label(self.table_frame, text=f"{val:.2f}", borderwidth=1, relief="solid", width=10)
            lbl.grid(row=row, column=col, sticky="nsew")

        self.label.config(text=f"Згенеровано {n} чисел. Відправка в Object3...")
        
        # Копіювання в буфер (за старою вимогою)
        clipboard_text = "\n".join(map(str, data_list))
        self.root.clipboard_clear()
        self.root.clipboard_append(clipboard_text)

        # АВТОМАТИЧНА ВІДПРАВКА В OBJECT3
        self.send_to_object3(data_list)

    def send_to_object3(self, data_list):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65433)) # Порт Object3
                s.sendall(json.dumps(data_list).encode('utf-8'))
                print("Дані відправлено в Object3")
        except ConnectionRefusedError:
            print("Object3 недоступний")

if __name__ == "__main__":
    root = tk.Tk()
    app = Object2App(root)
    root.mainloop()