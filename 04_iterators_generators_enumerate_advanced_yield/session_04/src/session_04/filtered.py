class EvenIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.numbers):
            num = self.numbers[self.index]
            self.index += 1
            if num % 2 == 0:
                return num
        raise StopIteration

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for number in EvenIterator(numbers):
    print(number)