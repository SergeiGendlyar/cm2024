import random
from math import gcd, isqrt

# Проверка числа на простоту
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Генерация случайного простого числа длиной n бит
def generate_prime(n):
    while True:
        p = random.randint(2**(n-1), 2**n - 1)
        if is_prime(p) and p % 4 == 1:  # Условие p ≡ 1 (mod 4)
            return p

# Проверка, является ли число квадратичным вычетом по модулю p
def is_quadratic_residue(a, p):
    return pow(a, (p - 1) // 2, p) == 1

# Нахождение квадратного корня из a по модулю p
def sqrt_mod(a, p):
    for x in range(p):
        if (x * x) % p == a:
            return x
    return None

# Умножение точки на эллиптической кривой
def point_multiplication(P, k, a, p):
    Q = None
    R = P
    while k:
        if k & 1:
            Q = point_addition(Q, R, a, p)
        R = point_addition(R, R, a, p)
        k >>= 1
    return Q

# Сложение двух точек на эллиптической кривой
def point_addition(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 != y2:
        return None

    if P == Q:
        s = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:
        s = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p

    return x3, y3

# Подсчёт количества точек на эллиптической кривой
def count_points(a, p):
    points = [None]  # Начинаем с точки на бесконечности
    for x in range(p):
        y_squared = (x**3 + a * x) % p
        if is_quadratic_residue(y_squared, p):
            y = sqrt_mod(y_squared, p)
            points.append((x, y))
            if y != 0:
                points.append((x, p - y))
    return points

# Проверка на цикличность группы
def is_group_cyclic(P, a, p, order):
    seen_points = set()
    Q = P
    for _ in range(order):
        if Q in seen_points:
            return False
        seen_points.add(Q)
        Q = point_addition(Q, P, a, p)
    return len(seen_points) == order

# Генерация эллиптической кривой
def generate_elliptic_curve(n):
    while True:
        print("\nГенерация случайного простого числа...")
        p = generate_prime(n)
        print(f"Сгенерировано простое число p = {p}, проверка p ≡ 1 (mod 4): успешно!")

        print("Подбор коэффициента a...")
        a = random.randint(1, p - 1)
        print(f"Выбран коэффициент a = {a}")

        print("Поиск базовой точки P0 на кривой...")
        P0 = None
        for x in range(p):
            y_squared = (x**3 + a * x) % p
            if is_quadratic_residue(y_squared, p):
                y = sqrt_mod(y_squared, p)
                P0 = (x, y)
                print(f"Найдена базовая точка P0: {P0}")
                break

        if P0 is None:
            print("Не удалось найти точку P0. Перегенерация параметров...\n")
            continue  # Если точка не найдена, начать заново

        print("Подсчёт точек на кривой...")
        points = count_points(a, p)
        num_points = len(points)
        print(f"Общее количество точек (включая бесконечность): {num_points}")

        print("Проверка теоремы Хассе...")
        lower_bound = p + 1 - 2 * isqrt(p)
        upper_bound = p + 1 + 2 * isqrt(p)
        if not (lower_bound <= num_points <= upper_bound):
            print(f"Порядок группы {num_points} не соответствует теореме Хассе. Перегенерация параметров...\n")
            continue

        print(f"Теорема Хассе выполнена: {lower_bound} <= {num_points} <= {upper_bound}")

        print("Проверка цикличности группы...")
        if not is_group_cyclic(P0, a, p, num_points):
            print("Группа не является циклической. Перегенерация параметров...\n")
            continue

        print("Группа является циклической! Эллиптическая кривая успешно сгенерирована.")
        return {
            "p": p,
            "a": a,
            "P0": P0,
            "points": points,
            "order": num_points
        }

# Ввод из консоли
def main():
    print("Алгоритм генерации эллиптической кривой")
    n = int(input("Введите длину простого числа (в битах): "))
    try:
        curve = generate_elliptic_curve(n)
        print("\nИтог:")
        print(f"Характеристика поля (p): {curve['p']}")
        print(f"Коэффициент кривой (a): {curve['a']}")
        print(f"Базовая точка P0: {curve['P0']}")
        print(f"Порядок группы: {curve['order']}")
        print(f"Точки группы (первые 10): {curve['points'][:10]}...")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
