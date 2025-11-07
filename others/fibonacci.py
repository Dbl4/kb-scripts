def fibonacci(n):
    if n < 2:
        return n

    return fibonacci(n-1) + fibonacci(n-2)


def fibonacci2(n, cache={}):
    if n in cache:
        return cache[n]

    if n < 2:
        return n

    return fibonacci2(n-1, cache) + fibonacci2(n-2, cache)

if __name__ == '__main__':
    print(fibonacci2(13))