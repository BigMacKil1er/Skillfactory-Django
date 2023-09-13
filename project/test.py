quote = "Do not give up, the beginning is always the hardest."
print(quote[8])

def make_dict(keys, values):
    result = {}
    for i, key in enumerate(keys):
        if i < len(values):
            result[key] = values[i]
        else:
            result[key] = None
    return result

# Пример использования функции:
keys = ["a", "b", "c"]
values = [1, 2]

result = make_dict(keys, values)
print(result)


def calculate(num1, num2, operation):
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "Деление на ноль невозможно"
    }

    result = operations.get(operation)
    if result:
        return result(num1, num2)
    else:
        return "Неизвестная операция"


# Примеры использования функции:
result1 = calculate(5, 3, '+')  # Сложение: 5 + 3 = 8
result2 = calculate(10, 4, '-')  # Вычитание: 10 - 4 = 6
result3 = calculate(6, 2, '*')  # Умножение: 6 * 2 = 12
result4 = calculate(8, 2, '/')  # Деление: 8 / 2 = 4
result5 = calculate(5, 0, '/')  # Деление на ноль: "Деление на ноль невозможно"
result6 = calculate(7, 5, '%')  # Неизвестная операция: "Неизвестная операция"

print(result1)
print(result2)
print(result3)
print(result4)
print(result5)
print(result6)