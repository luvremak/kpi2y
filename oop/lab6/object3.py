import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pyperclip

class Object3Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Object3 - Графік функції")
        self.root.geometry("1000x700")
        
        self.vector = None
        self.canvas = None
        self.fig = None
        
        success = self.read_from_clipboard()
        
        if success:
            self.create_widgets()
        
    def read_from_clipboard(self):
        try:
            clipboard_data = pyperclip.paste()
            
            if not clipboard_data or clipboard_data.strip() == "":
                raise ValueError("Буфер обміну порожній")
            
            lines = clipboard_data.strip().split('\n')
            values = []
            for line in lines:
                try:
                    values.append(float(line.strip()))
                except ValueError:
                    continue  
            
            self.vector = np.array(values)
            
            if len(self.vector) == 0:
                raise ValueError("Не знайдено числових даних")
            
            return True
                
        except Exception as e:
            messagebox.showerror("Помилка", 
                               f"Не вдалося зчитати дані з буфера обміну:\n{e}\n\n"
                               "Спочатку запустіть Object2 для генерації даних.")
            self.root.destroy()
            return False
            
    def create_widgets(self):
        title = tk.Label(self.root, 
                        text=f"Графік y = f(x) ({len(self.vector)} точок)", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        info_text = (f"Мін: {self.vector.min():.4f}  |  "
                    f"Макс: {self.vector.max():.4f}  |  "
                    f"Середнє: {self.vector.mean():.4f}  |  "
                    f"Станд. відхилення: {self.vector.std():.4f}")
        info = tk.Label(self.root, text=info_text, font=("Arial", 10))
        info.pack(pady=5)
        
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_plot()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        btn_refresh = tk.Button(btn_frame, text="Оновити з буфера", 
                               command=self.refresh_plot,
                               font=("Arial", 11), bg="#2196F3", fg="white",
                               padx=15, pady=8)
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        btn_save = tk.Button(btn_frame, text="Зберегти графік", 
                            command=self.save_plot,
                            font=("Arial", 11), bg="#FF9800", fg="white",
                            padx=15, pady=8)
        btn_save.pack(side=tk.LEFT, padx=5)
        
        btn_close = tk.Button(btn_frame, text="Закрити", 
                             command=self.root.destroy,
                             font=("Arial", 11), bg="#f44336", fg="white",
                             padx=15, pady=8)
        btn_close.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.root, 
                                     text="Дані успішно завантажено з буфера обміну", 
                                     font=("Arial", 9), fg="green")
        self.status_label.pack(pady=5)
        
    def create_plot(self):
        self.fig, ax = plt.subplots(figsize=(11, 6))
        
        x = np.arange(len(self.vector))
        y = self.vector
        
        ax.plot(x, y, 'b-', linewidth=2, label='y = f(x)', zorder=2)
        
        ax.plot(x, y, 'ro', markersize=4, zorder=3)
        
        ax.set_xlabel('x (індекс елемента)', fontsize=13, fontweight='bold')
        ax.set_ylabel('y (значення)', fontsize=13, fontweight='bold')
        ax.set_title('Графік функції y = f(x)', fontsize=15, fontweight='bold', pad=20)
        
        ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.8, zorder=1)
        
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        x_margin = max(1, len(self.vector) * 0.02)
        y_range = y.max() - y.min()
        y_margin = y_range * 0.1 if y_range > 0 else 1
        
        ax.set_xlim([-x_margin, len(self.vector) - 1 + x_margin])
        ax.set_ylim([y.min() - y_margin, y.max() + y_margin])
        
        if y.min() < 0 < y.max():
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.8, alpha=0.7)
        
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        
        self.fig.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def refresh_plot(self):
        try:
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                plt.close(self.fig)
            
            success = self.read_from_clipboard()
            
            if not success:
                return
            
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Label) and widget != self.status_label:
                    widget.destroy()
            
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            
            self.create_plot()
            
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.pack_forget()
            
            title = tk.Label(self.root, 
                            text=f"Графік y = f(x) ({len(self.vector)} точок)", 
                            font=("Arial", 14, "bold"))
            title.pack(pady=10, before=self.plot_frame)
            
            info_text = (f"Мін: {self.vector.min():.4f}  |  "
                        f"Макс: {self.vector.max():.4f}  |  "
                        f"Середнє: {self.vector.mean():.4f}  |  "
                        f"Станд. відхилення: {self.vector.std():.4f}")
            info = tk.Label(self.root, text=info_text, font=("Arial", 10))
            info.pack(pady=5, before=self.plot_frame)
            
            self.status_label.config(text="Графік оновлено з новими даними", fg="green")
            messagebox.showinfo("Успіх", "Графік оновлено з новими даними")
            
        except Exception as e:
            self.status_label.config(text=f"Помилка оновлення: {e}", fg="red")
            messagebox.showerror("Помилка", f"Не вдалося оновити графік:\n{e}")
    
    def save_plot(self):
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG файли", "*.png"), 
                          ("PDF файли", "*.pdf"),
                          ("Всі файли", "*.*")]
            )
            
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                self.status_label.config(text=f"Графік збережено: {filename}", fg="green")
                messagebox.showinfo("Успіх", f"Графік збережено у файл:\n{filename}")
        except Exception as e:
            self.status_label.config(text=f"Помилка збереження: {e}", fg="red")
            messagebox.showerror("Помилка", f"Не вдалося зберегти графік:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Object3Application(root)
    root.mainloop()