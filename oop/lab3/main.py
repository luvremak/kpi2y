from tkinter import Tk
from editor import GraphicEditor


def main():
    root = Tk()
    app = GraphicEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
