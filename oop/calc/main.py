"""
Модульний об'єктно-орієнтований калькулятор
Демонструє всі принципи ООП: інкапсуляція, наслідування, поліморфізм, абстракція
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union
import tkinter as tk
from tkinter import ttk


# ==================== АБСТРАКЦІЯ ====================
class NumberSystem(ABC):
    """Абстрактний базовий клас для системи числення"""
    
    @abstractmethod
    def to_decimal(self, value: str) -> int:
        """Конвертує з поточної системи в десяткову"""
        pass
    
    @abstractmethod
    def from_decimal(self, value: int) -> str:
        """Конвертує з десяткової в поточну систему"""
        pass
    
    @abstractmethod
    def validate(self, char: str) -> bool:
        """Перевіряє чи символ валідний для системи"""
        pass
    
    @abstractmethod
    def get_max_digits(self) -> int:
        """Максимальна кількість цифр"""
        pass


# ==================== НАСЛІДУВАННЯ та ПОЛІМОРФІЗМ ====================
class DecimalSystem(NumberSystem):
    """Десяткова система числення"""
    
    def to_decimal(self, value: str) -> int:
        return int(value) if value else 0
    
    def from_decimal(self, value: int) -> str:
        return str(value)
    
    def validate(self, char: str) -> bool:
        return char.isdigit() or char == '.'
    
    def get_max_digits(self) -> int:
        return 15


class BinarySystem(NumberSystem):
    """Двійкова система числення"""
    
    def to_decimal(self, value: str) -> int:
        return int(value, 2) if value else 0
    
    def from_decimal(self, value: int) -> str:
        return bin(value)[2:] if value >= 0 else bin(value)
    
    def validate(self, char: str) -> bool:
        return char in '01'
    
    def get_max_digits(self) -> int:
        return 32


class HexadecimalSystem(NumberSystem):
    """Шістнадцяткова система числення"""
    
    def to_decimal(self, value: str) -> int:
        return int(value, 16) if value else 0
    
    def from_decimal(self, value: int) -> str:
        return hex(value)[2:].upper() if value >= 0 else hex(value)
    
    def validate(self, char: str) -> bool:
        return char.upper() in '0123456789ABCDEF'
    
    def get_max_digits(self) -> int:
        return 8


# ==================== ENUM для типів операцій ====================
class OperationType(Enum):
    """Перелік типів операцій"""
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "×"
    DIVIDE = "/"
    NONE = ""


# ==================== ІНКАПСУЛЯЦІЯ ====================
class CalculatorState:
    """Клас для збереження стану калькулятора (інкапсуляція даних)"""
    
    def __init__(self):
        self.__current_value: str = "0"
        self.__stored_value: Optional[float] = None
        self.__operation: OperationType = OperationType.NONE
        self.__is_new_number: bool = True
        self.__number_system: NumberSystem = DecimalSystem()
    
    # Геттери та сеттери (інкапсуляція)
    @property
    def current_value(self) -> str:
        return self.__current_value
    
    @current_value.setter
    def current_value(self, value: str):
        self.__current_value = value
    
    @property
    def stored_value(self) -> Optional[float]:
        return self.__stored_value
    
    @stored_value.setter
    def stored_value(self, value: Optional[float]):
        self.__stored_value = value
    
    @property
    def operation(self) -> OperationType:
        return self.__operation
    
    @operation.setter
    def operation(self, op: OperationType):
        self.__operation = op
    
    @property
    def is_new_number(self) -> bool:
        return self.__is_new_number
    
    @is_new_number.setter
    def is_new_number(self, value: bool):
        self.__is_new_number = value
    
    @property
    def number_system(self) -> NumberSystem:
        return self.__number_system
    
    @number_system.setter
    def number_system(self, system: NumberSystem):
        self.__number_system = system
    
    def reset(self):
        """Скидання стану"""
        self.__current_value = "0"
        self.__stored_value = None
        self.__operation = OperationType.NONE
        self.__is_new_number = True


# ==================== СТРАТЕГІЯ для операцій ====================
class Operation(ABC):
    """Абстрактний клас для операцій (патерн Стратегія)"""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass


class AddOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")
        return a / b


# ==================== ФАБРИКА ====================
class OperationFactory:
    """Фабрика для створення операцій (патерн Фабрика)"""
    
    _operations = {
        OperationType.ADD: AddOperation(),
        OperationType.SUBTRACT: SubtractOperation(),
        OperationType.MULTIPLY: MultiplyOperation(),
        OperationType.DIVIDE: DivideOperation(),
    }
    
    @classmethod
    def get_operation(cls, op_type: OperationType) -> Optional[Operation]:
        return cls._operations.get(op_type)


# ==================== ОБЧИСЛЮВАЛЬНА ЛОГІКА ====================
class CalculatorEngine:
    """Двигун калькулятора - бізнес-логіка"""
    
    def __init__(self, state: CalculatorState):
        self._state = state
    
    def input_digit(self, digit: str):
        """Введення цифри"""
        if not self._state.number_system.validate(digit):
            return
        
        if self._state.is_new_number:
            self._state.current_value = digit
            self._state.is_new_number = False
        else:
            if len(self._state.current_value) < self._state.number_system.get_max_digits():
                if self._state.current_value == "0":
                    self._state.current_value = digit
                else:
                    self._state.current_value += digit
    
    def input_decimal(self):
        """Додавання десяткової крапки"""
        if not isinstance(self._state.number_system, DecimalSystem):
            return
        
        if self._state.is_new_number:
            self._state.current_value = "0."
            self._state.is_new_number = False
        elif "." not in self._state.current_value:
            self._state.current_value += "."
    
    def set_operation(self, operation: OperationType):
        """Встановлення операції"""
        if self._state.stored_value is not None and not self._state.is_new_number:
            self.calculate()
        
        try:
            self._state.stored_value = self._convert_to_decimal()
            self._state.operation = operation
            self._state.is_new_number = True
        except ValueError:
            self._state.current_value = "Помилка"
    
    def calculate(self):
        """Виконання обчислення"""
        if self._state.stored_value is None or self._state.operation == OperationType.NONE:
            return
        
        try:
            current = self._convert_to_decimal()
            operation = OperationFactory.get_operation(self._state.operation)
            
            if operation:
                result = operation.execute(self._state.stored_value, current)
                self._state.current_value = self._convert_from_decimal(result)
            
            self._state.stored_value = None
            self._state.operation = OperationType.NONE
            self._state.is_new_number = True
        except (ValueError, ZeroDivisionError) as e:
            self._state.current_value = "Помилка"
            self._state.reset()
    
    def reciprocal(self):
        """Обчислення 1/X"""
        try:
            value = self._convert_to_decimal()
            if value == 0:
                raise ValueError("Ділення на нуль")
            result = 1 / value
            self._state.current_value = self._convert_from_decimal(result)
            self._state.is_new_number = True
        except (ValueError, ZeroDivisionError):
            self._state.current_value = "Помилка"
    
    def negate(self):
        """Зміна знаку"""
        try:
            value = self._convert_to_decimal()
            result = -value
            self._state.current_value = self._convert_from_decimal(result)
        except ValueError:
            pass
    
    def backspace(self):
        """Видалення останнього символу"""
        if len(self._state.current_value) > 1:
            self._state.current_value = self._state.current_value[:-1]
        else:
            self._state.current_value = "0"
            self._state.is_new_number = True
    
    def clear(self):
        """Очищення"""
        self._state.reset()
    
    def change_number_system(self, system: NumberSystem):
        """Зміна системи числення"""
        try:
            decimal_value = self._convert_to_decimal()
            self._state.number_system = system
            self._state.current_value = self._convert_from_decimal(decimal_value)
        except ValueError:
            self._state.number_system = system
            self._state.current_value = "0"
    
    def _convert_to_decimal(self) -> float:
        """Конвертація в десяткове число"""
        if isinstance(self._state.number_system, DecimalSystem):
            return float(self._state.current_value)
        else:
            return float(self._state.number_system.to_decimal(self._state.current_value))
    
    def _convert_from_decimal(self, value: float) -> str:
        """Конвертація з десяткового числа"""
        if isinstance(self._state.number_system, DecimalSystem):
            # Видалення зайвих нулів
            result = f"{value:.10f}".rstrip('0').rstrip('.')
            return result if result != '-0' else '0'
        else:
            return self._state.number_system.from_decimal(int(value))


# ==================== GUI КОМПОНЕНТИ (Композиція) ====================
class DisplayWidget:
    """Віджет дисплею"""
    
    def __init__(self, parent):
        self.display = tk.Entry(
            parent,
            font=('Arial', 24, 'bold'),
            justify='right',
            bd=10,
            relief='sunken',
            state='readonly'
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    
    def update(self, value: str):
        """Оновлення дисплею"""
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, value)
        self.display.config(state='readonly')


class ButtonGrid:
    """Сітка кнопок"""
    
    def __init__(self, parent, button_callback):
        self.parent = parent
        self.callback = button_callback
        self._create_buttons()
    
    def _create_buttons(self):
        """Створення кнопок"""
        # Кнопки цифр та операцій
        buttons = [
            ('C', 1, 0, 'red'), ('←', 1, 1, 'orange'), ('1/X', 1, 2, 'blue'), ('/', 1, 3, 'green'),
            ('7', 2, 0, 'gray'), ('8', 2, 1, 'gray'), ('9', 2, 2, 'gray'), ('×', 2, 3, 'green'),
            ('4', 3, 0, 'gray'), ('5', 3, 1, 'gray'), ('6', 3, 2, 'gray'), ('-', 3, 3, 'green'),
            ('1', 4, 0, 'gray'), ('2', 4, 1, 'gray'), ('3', 4, 2, 'gray'), ('+', 4, 3, 'green'),
            ('±', 5, 0, 'blue'), ('0', 5, 1, 'gray'), ('.', 5, 2, 'gray'), ('=', 5, 3, 'darkgreen'),
        ]
        
        for (text, row, col, color) in buttons:
            btn = tk.Button(
                self.parent,
                text=text,
                font=('Arial', 18, 'bold'),
                bg=color,
                fg='white',
                command=lambda t=text: self.callback(t),
                height=2,
                width=5
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')


class ModeSelector:
    """Вибір режиму системи числення"""
    
    def __init__(self, parent, mode_callback):
        self.frame = ttk.LabelFrame(parent, text="Система числення", padding=10)
        self.frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
        
        self.mode_var = tk.StringVar(value="Десяткова")
        
        modes = [
            ("Десяткова", "DEC"),
            ("Двійкова", "BIN"),
            ("Шістнадцяткова", "HEX")
        ]
        
        for idx, (text, value) in enumerate(modes):
            rb = ttk.Radiobutton(
                self.frame,
                text=text,
                value=value,
                variable=self.mode_var,
                command=lambda v=value: mode_callback(v)
            )
            rb.grid(row=0, column=idx, padx=10)


# ==================== ГОЛОВНИЙ КЛАС (Фасад) ====================
class Calculator:
    """Головний клас калькулятора (патерн Фасад)"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Модульний ООП Калькулятор")
        self.root.resizable(False, False)
        
        # Ініціалізація компонентів
        self._state = CalculatorState()
        self._engine = CalculatorEngine(self._state)
        
        # Створення GUI
        self._setup_gui()
        self._configure_grid()
        
        # Оновлення дисплею
        self._update_display()
    
    def _setup_gui(self):
        """Налаштування GUI"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        self._display = DisplayWidget(main_frame)
        self._button_grid = ButtonGrid(main_frame, self._on_button_click)
        self._mode_selector = ModeSelector(main_frame, self._on_mode_change)
    
    def _configure_grid(self):
        """Налаштування сітки"""
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def _on_button_click(self, button_text: str):
        """Обробка натискання кнопки"""
        if button_text.isdigit():
            self._engine.input_digit(button_text)
        elif button_text == '.':
            self._engine.input_decimal()
        elif button_text == 'C':
            self._engine.clear()
        elif button_text == '←':
            self._engine.backspace()
        elif button_text == '±':
            self._engine.negate()
        elif button_text == '1/X':
            self._engine.reciprocal()
        elif button_text == '=':
            self._engine.calculate()
        elif button_text in ['+', '-', '×', '/']:
            op_map = {
                '+': OperationType.ADD,
                '-': OperationType.SUBTRACT,
                '×': OperationType.MULTIPLY,
                '/': OperationType.DIVIDE
            }
            self._engine.set_operation(op_map[button_text])
        
        self._update_display()
    
    def _on_mode_change(self, mode: str):
        """Обробка зміни режиму"""
        system_map = {
            'DEC': DecimalSystem(),
            'BIN': BinarySystem(),
            'HEX': HexadecimalSystem()
        }
        self._engine.change_number_system(system_map[mode])
        self._update_display()
    
    def _update_display(self):
        """Оновлення дисплею"""
        self._display.update(self._state.current_value)
    
    def run(self):
        """Запуск калькулятора"""
        self.root.mainloop()


# ==================== ТОЧКА ВХОДУ ====================
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    calculator.run()