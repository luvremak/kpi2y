import math

class CalculatorModel:

    def __init__(self):
        self.current_expression = ""
        self.mode = "DEC"  # Варіанти: DEC, BIN, HEX

    def add_character(self, char):
        """Додає символ до виразу."""
        self.current_expression += str(char)

    def backspace(self):
        """Видаляє останній символ."""
        self.current_expression = self.current_expression[:-1]

    def clear(self):
        """Очищує вираз."""
        self.current_expression = ""

    def calculate(self):
        """Обчислює математичний вираз."""
        try:
            result = eval(self.current_expression)
            return self._format_result(result)
        except Exception:
            return "Error"

    def calculate_special(self, operation):
        """Обробляє спеціальні операції (1/x, ±)."""
        try:
            if not self.current_expression:
                return

            val = self._parse_current_value()

            if operation == "1/x":
                if val == 0:
                    self.current_expression = "Error"
                else:
                    res = 1 / val
                    self.current_expression = self._format_result(res)
            
            elif operation == "±":
                res = -val
                self.current_expression = self._format_result(res)

        except Exception:
            self.current_expression = "Error"

    def _parse_current_value(self):
        """Парсинг поточного рядка в число залежно від режиму."""
        if self.mode == "HEX":
            return int(self.current_expression, 16)
        elif self.mode == "BIN":
            return int(self.current_expression, 2)
        else:
            return float(self.current_expression)

    def _format_result(self, value):
        """Форматування результату назад у рядок відповідно до режиму."""
        try:
            if self.mode == "HEX":
                return hex(int(value))[2:].upper()
            elif self.mode == "BIN":
                return bin(int(value))[2:]
            else:
                if isinstance(value, float) and value.is_integer():
                    return str(int(value))
                return str(value)
        except:
            return "Error"

    def switch_mode(self, new_mode):
        """Змінює режим та конвертує поточне число."""
        if self.current_expression == "" or self.current_expression == "Error":
            self.mode = new_mode
            return

        try:
            current_val = self._parse_current_value()
            self.mode = new_mode
            self.current_expression = self._format_result(current_val)
        except:
            self.current_expression = "Error"
            self.mode = new_mode