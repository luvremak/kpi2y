import tkinter as tk
from calculator import CalculatorModel

class CalculatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Modular Calculator")
        self.root.geometry("400x600")
        
        # Ініціалізація моделі
        self.model = CalculatorModel()

        # Змінні GUI
        self.display_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="DEC")

        self._create_display()
        self._create_mode_selectors()
        self._create_buttons()
        
        # Початковий стан кнопок
        self._update_button_states("DEC")

    def _create_display(self):
        display = tk.Entry(self.root, textvariable=self.display_var, 
                           font=("Arial", 24), bd=10, insertwidth=2, width=14, justify='right')
        display.pack(fill=tk.BOTH, ipadx=8, padx=10, pady=10)

    def _create_mode_selectors(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        
        modes = [("Decimal", "DEC"), ("Binary", "BIN"), ("Hex", "HEX")]
        
        for text, mode in modes:
            b = tk.Radiobutton(frame, text=text, variable=self.mode_var, 
                               value=mode, command=self._on_mode_change)
            b.pack(side=tk.LEFT, padx=10)

    def _create_buttons(self):
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack()

        buttons = [
            ('C', 0, 0), ('←', 0, 1), ('1/x', 0, 2), ('±', 0, 3),
            ('D', 1, 0), ('E', 1, 1), ('F', 1, 2), ('/', 1, 3),
            ('A', 2, 0), ('B', 2, 1), ('C', 2, 2, "HEX_C"),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('×', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2)
        ]

        self.btn_widgets = {}

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            key = text if len(btn) <= 3 else btn[3]

            cmd = lambda x=text: self._on_button_click(x)
            
            b = tk.Button(self.btn_frame, text=text, font=("Arial", 14), 
                          width=5, height=2, command=cmd)
            b.grid(row=row, column=col, padx=2, pady=2)
            self.btn_widgets[key] = b
            
            if text == '=':
                b.grid(columnspan=2, sticky="nsew")
                b.config(bg="lightblue")

    def _on_mode_change(self):
        new_mode = self.mode_var.get()
        self.model.switch_mode(new_mode)
        self._update_display()
        self._update_button_states(new_mode)

    def _update_button_states(self, mode):
        hex_digits = ['A', 'B', 'HEX_C', 'D', 'E', 'F']
        non_bin_digits = ['2', '3', '4', '5', '6', '7', '8', '9'] + hex_digits
        
        # Скидаємо стан усіх кнопок
        for k in self.btn_widgets:
            self.btn_widgets[k].config(state=tk.NORMAL)

        if mode == "BIN":
            for k in non_bin_digits: self.btn_widgets[k].config(state=tk.DISABLED)
            self.btn_widgets['.'].config(state=tk.DISABLED)
        elif mode == "DEC":
            for k in hex_digits: self.btn_widgets[k].config(state=tk.DISABLED)
        elif mode == "HEX":
            self.btn_widgets['.'].config(state=tk.DISABLED)

    def _on_button_click(self, char):
        if char == 'C':
            self.model.clear()
        elif char == '←':
            self.model.backspace()
        elif char == '=':
            res = self.model.calculate()
            self.model.current_expression = str(res)
        elif char == '1/x':
            self.model.calculate_special('1/x')
        elif char == '±':
            self.model.calculate_special('±')
        elif char == '×':
            self.model.add_character('*')
        else:
            self.model.add_character(char)
        
        self._update_display()

    def _update_display(self):
        self.display_var.set(self.model.current_expression)