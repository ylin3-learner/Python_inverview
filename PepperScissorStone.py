import random


# game_list = ['剪刀', '石頭', '布']
#
# user_input = int(input("請輸入: [0. 剪刀 1. 石頭 2. 布]"))
# computer_choice = random.randint(0, 2)
#
# # 石頭 > 剪刀
# # 布 > 石頭
# # 剪刀 > 布
#
# while True:
#     if user_input != computer_choice:
#         if user_input == 0 and computer_choice != 1:
#             print(f"你贏了! 你: {game_list[user_input]}, 電腦: {game_list[computer_choice]}")
#             break
#         elif user_input == 1 and computer_choice != 2:
#             print(f"你贏了! 你: {game_list[user_input]}, 電腦: {game_list[computer_choice]}")
#             break
#         elif user_input == 2 and computer_choice != 0:
#             print(f"你贏了! 你: {game_list[user_input]}, 電腦: {game_list[computer_choice]}")
#             break
#         else:
#             print(f"你輸了! 你: {game_list[user_input]}, 電腦: {game_list[user_input]}")
#             break
#
#     else:
#         print("Please try another time, your choice is the same as computer.\n")
#         break

'''
改進版代碼:
1. 如果使用者輸入的數字不在 0、1、2 範圍內，程式會出錯。在輸入後先加入檢查，如果不在範圍內，要求使用者重新輸入。
2. 在比較石頭、剪刀、布的大小時，可以將每個選項轉換成數字，這樣比較時會比較容易。
3. 使用bool來代表勝負，簡化了比較的過程。
4. 將整個遊戲放在無窮迴圈中
'''

options = {0: '剪刀', 1: '石頭', 2: '布'}

while True:
    user_input = input("請輸入: [0. 剪刀 1. 石頭 2. 布]")

    try:
        user_input = int(user_input)
        if user_input not in options:
            print("輸入錯誤! 請輸入0, 1 或 2")
    except Exception as e:
        print(f"輸入非法! 你輸入:{user_input} ", e)
        continue

    computer_random_number = random.randint(0, 2)

    user_choice = options[user_input]
    computer_choice = options[computer_random_number]

    if user_choice == computer_choice:
        print("平手, 再試一次!\n")

    elif (user_choice == '剪刀' and computer_choice == '布') or \
         (user_choice == '石頭' and computer_choice == '剪刀') or \
         (user_choice == '布' and computer_choice == '石頭'):
        print(f"你贏了! 你: {user_choice}, 電腦: {computer_choice}\n")
    else:
        print(f"你輸了! 你: {user_choice}, 電腦: {computer_choice}\n")

    play_again = input("再玩一次? (y/n):").lower()
    if play_again != 'y':
        break
