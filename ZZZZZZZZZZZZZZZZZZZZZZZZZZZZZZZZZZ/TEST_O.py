def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


def print_primes(n, width):
    count = 0
    for i in range(2, n + 1):
        if is_prime(i):
            if count % width == 0 and count != 0:
                print()
            print(f"{i:{width}}", end=' ')
            count += 1
    print("\nTotal prime numbers found:", count)


if __name__ == "__main__":
    n = int(input("Введите число: "))
    print_primes(n, 8)