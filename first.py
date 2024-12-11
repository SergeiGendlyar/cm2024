import random
from math import gcd, isqrt
import matplotlib.pyplot as plt

# Проверка числа на простоту
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Генерация всех простых чисел длиной n бит
def generate_primes(n):
    primes = []
    for p in range(2**(n-1), 2**n):
        if is_prime(p) and p % 4 == 1:  # Условие p ≡ 1 (mod 4)
            primes.append(p)
    return primes

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
    R = None
    Q = P

    while k > 0:
        if k % 2 == 1:  # Если текущий бит равен 1
            R = point_addition(R, Q, a, p)
            if R is None:
                return None
        Q = point_addition(Q, Q, a, p)
        if Q is None:
            return None
        k //= 2
    return R


# Сложение двух точек на эллиптической кривой
def point_addition(P, Q, a, p):
    if P is None:  # Точка на бесконечности
        return Q
    if Q is None:  # Точка на бесконечности
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == -y2 % p:
        return None  # Сложение противоположных точек приводит к точке на бесконечности

    if P == Q:  # Удвоение точки
        if y1 % p == 0:  # Нет обратного элемента для 2y1
            return None
        s = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:  # Сложение двух разных точек
        if (x2 - x1) % p == 0:  # Нет обратного элемента для x2 - x1
            return None
        s = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3

# Подсчёт количества точек на эллиптической кривой
def count_points(a, p):
    points = [None]  # Точка на бесконечности
    for x in range(p):
        y_squared = (x**3 + a * x) % p
        if is_quadratic_residue(y_squared, p):
            y = sqrt_mod(y_squared, p)
            points.append((x, y))
            if y != 0:
                points.append((x, p - y))
    return points

# Нахождение порядка подгруппы, порождённой P0
def find_order(P0, a, p):
    if P0 is None:
        return None
    Q = P0
    for i in range(1, p + 1):  # Порядок не может превышать p + 1
        Q = point_multiplication(P0, i, a, p)
        if Q is None:  # Достигли точки на бесконечности
            return i
    return None  # Если не удалось найти порядок

# Проверка на цикличность группы
def is_group_cyclic(P, a, p, order):
    seen_points = set()
    Q = P
    for index in range(order):
        if Q in seen_points:
            return False
        seen_points.add(Q)
        Q = point_addition(Q, P, a, p)
    return len(seen_points) == order


# Построение графика эллиптической кривой
def plot_curve(points, p, a):
    # Исключаем точки на бесконечности (None) из списка для графика
    valid_points = [(x, y) for pt in points if pt is not None for x, y in [pt]]

    if not valid_points:
        print("Нет точек для отображения на графике.")
        return

    x_vals, y_vals = zip(*valid_points)

    plt.figure(figsize=(8, 6))
    plt.scatter(x_vals, y_vals, c='blue', label='Точки на кривой')
    plt.title(f"Эллиптическая кривая: y^2 = x^3 + {a}x (mod {p})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()


# Добавление функции разложения в кольце Z[i]
def decompose_in_zi(p):
    for d in range(1, isqrt(p) + 1):
        e_squared = p - d ** 2
        if e_squared >= 0:
            e = isqrt(e_squared)
            if e ** 2 == e_squared:
                return (d, e)
    return None


# Изменение функции генерации эллиптической кривой
def generate_elliptic_curve(n):
    primes = generate_primes(n)
    if not primes:
        print("Не найдено подходящих простых чисел для заданной длины n.")
        return None

    random.shuffle(primes)  # Перемешиваем массив простых чисел

    for p in primes:
        print(f"\nТекущая характеристика поля: p = {p}")

        # Разложение числа p в кольце Z[i]
        decomposition = decompose_in_zi(p)
        if decomposition:
            d, e = decomposition
            print(f"Разложение числа p в Z[i]: p = ({d} + {e}i)({d} - {e}i), где d^2 + e^2 = {p}")
        else:
            print(f"Не удалось разложить p = {p} в Z[i]. Пропускаем это число.")
            continue

        for attempt in range(10):  # Ограничиваем количество попыток для подбора a
            a = random.randint(1, p - 1)
            print(f"Подобран коэффициент a = {a}")

            # Проверка условия следствия 2 (например, -a — квадратичный вычет)
            if pow(-a, (p - 1) // 2, p) == 1:
                print(f"-a является квадратичным вычетом в GF({p}).")
                h = 2 * d
            else:
                print(f"-a не является квадратичным вычетом в GF({p}).")
                h = 2 * e

            # Расчёт количества точек на эллиптической кривой
            num_points = p + 1 + h
            print(f"Количество точек на кривой E(GF(p)): {num_points}")

            P0 = None
            for x in range(p):
                y_squared = (x ** 3 + a * x) % p
                if is_quadratic_residue(y_squared, p):
                    y = sqrt_mod(y_squared, p)
                    P0 = (x, y)
                    print(f"Найдена базовая точка P0: {P0}")
                    break

            if P0 is None:
                print(f"Не удалось найти базовую точку для p = {p}, a = {a}. Пробуем другое значение a.")
                continue

            points = count_points(a, p)
            print(f"Порядок группы (включая бесконечность): {len(points)}")

            # Проверяем порядок подгруппы, порождённой P0
            q = find_order(P0, a, p)
            if q is None:
                print(f"Не удалось найти порядок подгруппы для P0 = {P0}. Пробуем другое значение.")
                continue

            if not is_group_cyclic(P0, a, p, q):
                print(f"Группа, порождённая P0, не является циклической для p = {p}, a = {a}.")
                continue

            print(f"Сгенерирована эллиптическая кривая при p = {p}:")
            return {
                "p": p,
                "a": a,
                "P0": P0,
                "points": points,
                "order": len(points),
                "subgroup_order": q
            }

    print("Не удалось сгенерировать эллиптическую кривую для всех возможных простых чисел.")
    return None


# Обновление основной функции
def main():
    print("Алгоритм генерации эллиптической кривой")
    n = int(input("Введите длину простого числа (в битах): "))
    curve = generate_elliptic_curve(n)

    if curve:
        print("\nИтоговые параметры эллиптической кривой:")
        print(f"Характеристика поля (p): {curve['p']}")
        print(f"Коэффициент кривой (a): {curve['a']}")
        print(f"Базовая точка P0: {curve['P0']}")
        print(f"Порядок группы (включая бесконечность): {curve['order']}")
        print(f"Порядок подгруппы (q): {curve['subgroup_order']}")
        plot_curve(curve['points'], curve['p'], curve['a'])
    else:
        print("Не удалось сгенерировать эллиптическую кривую для заданной длины n.")


if __name__ == "__main__":
    main()