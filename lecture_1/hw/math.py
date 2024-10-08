async def factorial(n: int):
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


async def fibonacci(n: int):
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


async def mean(values: list):
    return sum(values) / len(values)