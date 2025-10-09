import tkinter as tk

def create_tooltip(widget, text):
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=text, background="lightyellow",
                         relief=tk.SOLID, borderwidth=1, padx=5, pady=2)
        label.pack()
        widget.tooltip = tooltip

    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip

    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)
