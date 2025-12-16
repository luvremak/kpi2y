import tkinter as tk
import socket
import json
import threading
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Object3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Object3 - Графік (Port 65433)")
        self.root.geometry("500x400+820+100")

        self.status_lbl = tk.Label(root, text="Очікування даних від Object2...", fg="blue")
        self.status_lbl.pack(pady=5)

        # Налаштування Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.gui_queue = queue.Queue()
        self.root.after(100, self.process_queue)

        # Запуск сервера
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

    def start_server(self):
        HOST = '127.0.0.1'
        PORT = 65433
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    data_raw = conn.recv(4096 * 4) # Збільшений буфер для великих масивів
                    if data_raw:
                        data_list = json.loads(data_raw.decode('utf-8'))
                        self.gui_queue.put(data_list)

    def process_queue(self):
        try:
            while True:
                data = self.gui_queue.get_nowait()
                self.update_graph(data)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def update_graph(self, data):
        self.status_lbl.config(text=f"Отримано {len(data)} точок. Графік оновлено.")
        
        self.ax.clear()
        sorted_data = sorted(data)
        x_values = list(range(len(sorted_data)))
        
        self.ax.plot(x_values, sorted_data, marker='.', color='r', linestyle='-')
        self.ax.set_title("Графік y=f(x)")
        self.ax.grid(True)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = Object3App(root)
    root.mainloop()