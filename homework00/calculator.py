import math
import typing as tp


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "*":
        return num_1 * num_2
    if command == ":":
        return round((num_1 / num_2), 1)
    if command == "^2":
        return num_1**2
    if command == "^":
        return num_1**num_2
    if command == "sin":
        return round(math.sin(math.radians(num_1)), 1)
    if command == "cos":
        return round(math.cos(math.radians(num_1)), 1)
    if command == "tg":
        return round(math.tan(math.radians(num_1)), 1)
    if command == "ln":
        if num_1 <= 0:
            return "Ошибка"
        return round(math.log(num_1), 1)
    if command == "lg":
        if num_1 <= 0:
            return "Ошибка"
        return round(math.log10(num_1), 1)
    return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:  # программа выполняется до ввода 0 вместо команды
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND in ("^2", "sin", "cos", "tg", "ln", "lg"):
            NUM_1 = float(input("Первое число > "))
            print(calc(NUM_1, 0, COMMAND))
        else:
            NUM_1 = float(input("Первое число > "))
            NUM_2 = float(input("Второе число > "))
            print(calc(NUM_1, NUM_2, COMMAND))
