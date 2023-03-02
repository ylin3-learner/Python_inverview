import math

def quadratic_formula(a, b, c):
    """
    計算一元二次方程式的解
    """
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None
    elif discriminant == 0:
        return - b / (2 * a)
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return x1, x2


a = float(input("請輸入一元二次方程的a值："))
b = float(input("請輸入一元二次方程的b值："))
c = float(input("請輸入一元二次方程的c值："))

result = quadratic_formula(a, b, c)

if result is None:
    print("此方程無實數解")
elif isinstance(result, float):
    print("此方程有唯一實根：", result)
else:
    print("此方程有兩個實根：", result[0], "和", result[1])