import random
class Cat:
    # Аттрибут - некоторая информация
    # Метод - некоторая функция по работе с атрибутами

    # Конструктор - метод создания нового объекта
    def __init__(self, name: str):
        self.name = name
        self.energy = random.randint(50, 100)

    # Есть 3 состояния
    # Первое - все ок (0)
    # Второе - перекормлен (1)
    # Третье - Нужно зарядить (2)
    def get_status(self):
        if self.energy >= 100:
            return 1
        elif self.energy == 0:
            return 2
        else:
            return 0

    def meow(self):
        if self.get_status() == 0:
            print(f"{self.name} - meow!")
            self.energy -= 1

    def feed(self, amount: int):
        if self.get_status() == 0:
            self.energy += amount
            print(f"{self.name} - Thank you!")

    def __repr__(self):
        return f"Cat(name={self.name}, energy={self.energy})"
