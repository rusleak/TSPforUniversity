import math


class Coordinates:
    def __init__(self, number ,x, y):
        self.number = number
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.number}: ({self.x}, {self.y})'

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
    pass