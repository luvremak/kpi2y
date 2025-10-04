import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

class Lab1App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lab1")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.center_window(self.root, 400, 300)
        
        self.create_main_menu()
        
        self.selected_number = 50
        
        self.dialog1 = None
        self.dialog2 = None
    
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_label = tk.Label(self.root, text="Lab1", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        variant1_btn = tk.Button(self.root, text="Варіант 1: Діалог з повзунком", 
                                width=30, height=2, command=self.show_variant1)
        variant1_btn.pack(pady=10)
        
        variant2_btn = tk.Button(self.root, text="Варіант 2: Послідовні діалоги", 
                                width=30, height=2, command=self.show_variant2)
        variant2_btn.pack(pady=10)
        
        exit_btn = tk.Button(self.root, text="Вихід", width=15, command=self.root.quit)
        exit_btn.pack(pady=20)
    
    def show_variant1(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_label = tk.Label(self.root, text="Варіант 1: Діалог з повзунком", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        self.number_display = tk.Label(self.root, text=f"Вибране число: {self.selected_number}", 
                                      font=("Arial", 12), bg="lightblue", 
                                      width=30, height=3, relief="sunken")
        self.number_display.pack(pady=20)
        
        dialog_btn = tk.Button(self.root, text="Відкрити діалог з повзунком", 
                              width=25, height=2, command=self.open_scroll_dialog)
        dialog_btn.pack(pady=10)
        
        back_btn = tk.Button(self.root, text="Назад до меню", 
                            width=15, command=self.create_main_menu)
        back_btn.pack(pady=10)
    
    def open_scroll_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Виберіть число")
        dialog.geometry("350x180")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        self.center_window(dialog, 350, 180)
        
        label = tk.Label(dialog, text="Виберіть число від 1 до 100:")
        label.pack(pady=10)
        
        scale_var = tk.IntVar(value=self.selected_number)
        scale = tk.Scale(dialog, from_=1, to=100, orient=tk.HORIZONTAL, 
                        variable=scale_var, length=200)
        scale.pack(pady=5)
        
        current_label = tk.Label(dialog, text=f"Поточне значення: {self.selected_number}")
        current_label.pack(pady=5)
        
        def update_label():
            current_label.config(text=f"Поточне значення: {scale_var.get()}")
            dialog.after(100, update_label)
        
        update_label()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def on_ok():
            self.selected_number = scale_var.get()
            self.number_display.config(text=f"Вибране число: {self.selected_number}")
            dialog.destroy()
        
        ok_btn = tk.Button(button_frame, text="Так", width=15, height=2, 
                          font=("Arial", 10), command=on_ok)
        ok_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="Відміна", width=15, height=2,
                              font=("Arial", 10), command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_variant2(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_label = tk.Label(self.root, text="Варіант 2: Послідовні діалоги", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        self.status_display = tk.Label(self.root, text="Натисніть кнопку нижче для початку", 
                                      font=("Arial", 12), bg="lightgreen", 
                                      width=40, height=3, relief="sunken")
        self.status_display.pack(pady=20)
        
        dialog_btn = tk.Button(self.root, text="Відкрити перший діалог", 
                              width=25, height=2, command=self.open_first_dialog)
        dialog_btn.pack(pady=10)
        
        back_btn = tk.Button(self.root, text="Назад до меню", 
                            width=15, command=self.create_main_menu)
        back_btn.pack(pady=10)
    
    def open_first_dialog(self):
        if self.dialog1 is not None and self.dialog1.winfo_exists():
            self.dialog1.lift()
            return
            
        self.dialog1 = tk.Toplevel(self.root)
        self.dialog1.title("Перший діалог")
        self.dialog1.geometry("280x130")
        self.dialog1.resizable(False, False)
        self.dialog1.grab_set()
        
        self.center_window(self.dialog1, 280, 130)
        
        label = tk.Label(self.dialog1, text="Це перший діалог")
        label.pack(pady=10)
        
        button_frame = tk.Frame(self.dialog1)
        button_frame.pack(pady=10)
        
        next_btn = tk.Button(button_frame, text="Далі >", width=15, height=2,
                            font=("Arial", 10), command=self.open_second_dialog)
        next_btn.pack(side=tk.LEFT, padx=10)
        
        def on_cancel1():
            self.status_display.config(text="Перший діалог скасовано")
            self.dialog1.destroy()
        
        cancel_btn = tk.Button(button_frame, text="Відміна", width=15, height=2,
                              font=("Arial", 10), command=on_cancel1)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def open_second_dialog(self):
        if self.dialog1 and self.dialog1.winfo_exists():
            self.dialog1.withdraw()
        
        self.dialog2 = tk.Toplevel(self.root)
        self.dialog2.title("Другий діалог")
        self.dialog2.geometry("380x130")
        self.dialog2.resizable(False, False)
        self.dialog2.grab_set()
        
        self.center_window(self.dialog2, 380, 130)
        
        label = tk.Label(self.dialog2, text="Це другий діалог")
        label.pack(pady=10)
        
        button_frame = tk.Frame(self.dialog2)
        button_frame.pack(pady=10)
        
        def go_back():
            self.dialog2.destroy()
            if self.dialog1 and self.dialog1.winfo_exists():
                self.dialog1.deiconify()
                self.dialog1.grab_set()
        
        back_btn = tk.Button(button_frame, text="< Назад", width=12, height=2,
                            font=("Arial", 10), command=go_back)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        def on_ok2():
            self.status_display.config(text="Другий діалог завершено успішно!")
            self.dialog2.destroy()
            if self.dialog1 and self.dialog1.winfo_exists():
                self.dialog1.destroy()
        
        ok_btn = tk.Button(button_frame, text="Так", width=12, height=2,
                          font=("Arial", 10), command=on_ok2)
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        def on_cancel2():
            self.status_display.config(text="Другий діалог скасовано")
            self.dialog2.destroy()
            if self.dialog1 and self.dialog1.winfo_exists():
                self.dialog1.destroy()
        
        cancel_btn = tk.Button(button_frame, text="Відміна", width=12, height=2,
                              font=("Arial", 10), command=on_cancel2)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Lab1App()
    app.run()