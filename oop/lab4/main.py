import tkinter as tk
from .editor import MyEditor

def main():
    root = tk.Tk()

    editor = MyEditor(root)

    root.mainloop()

if __name__ == "__main__":
    main()