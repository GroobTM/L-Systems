class Stack:
    __stack = []

    def push(self, value):
        self.__stack.append(value)

    def pop(self):
        return self.__stack.pop()