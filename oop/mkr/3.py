import random

# -----------------------------
# Classic Singleton
# -----------------------------
class SmartKettle1:
    _instance = None

    def __new__(cls, name="Smart Kettle 1"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.water_level = 0
            cls._instance.temperature = 20
        return cls._instance

    def boil(self):
        self.temperature = 100
        print(f"{self.name} is boiling! Temp: {self.temperature}°C.")

    def pour_tea(self):
        if self.water_level > 0 and self.temperature >= 80:
            print(f"{self.name} pours a cup of tea!")
            self.water_level -= 1
        else:
            print(f"{self.name} cannot pour tea. Add water or boil it.")


# -----------------------------
# Lazy Singleton
# -----------------------------
class SmartKettle2:
    _instance = None

    def __init__(self, name="Smart Kettle 2"):
        self.name = name
        self.water_level = 2
        self.temperature = 20

    @classmethod
    def get_instance(cls, name=None):
        if cls._instance is None:
            cls._instance = cls(name if name else "Smart Kettle 2")
        return cls._instance

    def boil(self):
        self.temperature = 100
        print(f"{self.name} is boiling! Temp: {self.temperature}°C.")

    def pour_tea(self):
        if self.water_level > 0 and self.temperature >= 80:
            print(f"{self.name} pours a cup of tea!")
            self.water_level -= 1
        else:
            print(f"{self.name} cannot pour tea. Add water or boil it.")


# -----------------------------
# Singleton через метаклас
# -----------------------------
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SmartKettle3(metaclass=SingletonMeta):
    def __init__(self, name="Smart Kettle 3"):
        self.name = name
        self.water_level = 3
        self.temperature = 20

    def boil(self):
        self.temperature = 100
        print(f"{self.name} is boiling! Temp: {self.temperature}°C.")

    def pour_tea(self):
        if self.water_level > 0 and self.temperature >= 80:
            print(f"{self.name} pours a cup of tea!")
            self.water_level -= 1
        else:
            print(f"{self.name} cannot pour tea. Add water or boil it.")


# -----------------------------
# Демонстрація
# -----------------------------
print("=== Classic Singleton ===")
k1 = SmartKettle1()
k2 = SmartKettle1()
k1.water_level = 2
k1.boil()
k2.pour_tea()
print(f"k1 is k2: {k1 is k2}\n")

print("=== Lazy Singleton ===")
lazy1 = SmartKettle2.get_instance()
lazy2 = SmartKettle2.get_instance()
lazy1.boil()
lazy2.pour_tea()
print(f"lazy1 is lazy2: {lazy1 is lazy2}\n")

print("=== Metaclass Singleton ===")
meta1 = SmartKettle3()
meta2 = SmartKettle3()
meta1.boil()
meta2.pour_tea()
print(f"meta1 is meta2: {meta1 is meta2}")
