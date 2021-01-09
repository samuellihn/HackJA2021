class Counter:
    def __init__(self, initialvalue=0):
        self.count = initialvalue

    def add(self, value):
        self.count += value

    def subtract(self, value):
        self.count -= value

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def __int__(self):
        return self.count
