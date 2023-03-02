def calculate_trapezoid_area(upper_base, down_case, height):
    return (upper_base + down_case) * height / 2

def get_input():

    while True:
        try:
            upper_base = int(input("請輸入梯形的上底長度："))
            down_base = int(input("請輸入梯形的下底長度："))
            height = int(input("請輸入梯形的高長度："))
        except ValueError:
            print("輸入有誤, 請重新輸入")
            continue

        if upper_base <= 0 or down_base <= 0 or height <= 0:
            print("梯形的輸入必須大於0，請重新輸入")
            continue

        return upper_base, down_base, height


def main():
    # get user_input
    inputs = get_input()
    if inputs is None:
        return

    upper_base, down_base, height = inputs

    # calculate trapezoid area
    area = calculate_trapezoid_area(upper_base, down_base, height)

    print("梯形面積為: ", area)


if __name__ == '__main__':
    main()
