def factorial(n):
    result = 1
    i = 1
    while i <= n:
        result *= i
        i += 1
    return result


def fibonacci(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def classify(value):
    match value % 3:
        case 0:
            label = "fizz"
        case 1:
            label = "one"
        case _:
            label = "other"
    return label


def find_max(values):
    max_val = values[0]
    for v in values:
        if v > max_val:
            max_val = v
    return max_val


def count_positive(values):
    count = 0
    i = 0
    while i < len(values):
        if values[i] > 0:
            count += 1
        i += 1
    return count


result = factorial(5)
fib = fibonacci(10)
nums = [3, 1, 4, 1, 5, 9, 2, 6]
biggest = find_max(nums)
pos = count_positive(nums)
label = classify(7)
