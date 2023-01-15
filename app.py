# coding:utf-8

# 管理使用平台的輸入輸出
import time

from colorama import Fore, Style
from getpass import getpass
from service.user_service import UserService
from service.news_service import NewsService
from service.role_service import RoleService
from service.type_service import TypeService

import os
import sys

__user_service = UserService()
__news_service = NewsService()
__role_service = RoleService()
__type_service = TypeService()

while True:
    os.system('cls')  # 清空指令
    print(Fore.LIGHTBLUE_EX, "\n\t==========")
    print("\n\t歡迎使用新聞管理系統")
    print(Fore.LIGHTGREEN_EX, "\n\t==========")
    print("\n\t1.登錄系統")
    print("\n\t2.退出系統")
    print(Style.RESET_ALL)
    opt = input("\n\t輸入操作編號：")  # 在這其中寫的數據將保存到opt裡, 變成str類型

    if opt == '1':
       username = input('\n\t請輸入用戶名：')
       password = getpass('\n\t請輸入密碼：')  # 隱去密碼, 不能使用input, 而是getpass
       result = __user_service.login(username, password)
        # 查詢角色
       if result == True:
           role = __user_service.search_user_role(username)
           while True:  # 每一層都要死循環
               os.system('cls')  # 二級菜單時, 系統選項應清空
               if role == '新聞編輯':
                   # print(Fore.LIGHTRED_EX, '\n\t新聞編輯模塊正在開發中------')
                   # print('\n\t(3秒後自動返回)')
                   # time.sleep(3)
                   # break
                   print(Fore.LIGHTBLUE_EX, '\n\t1.發表新聞')
                   print(Fore.LIGHTBLUE_EX, '\n\t2.編輯新聞')
                   print(Fore.LIGHTGREEN_EX, "\n\tback.退出登錄")
                   print(Fore.LIGHTGREEN_EX, "\n\texit.退出系統")
                   print(Style.RESET_ALL)
                   choice = input('\n\t輸入操作編號：')
                   if choice == '1':
                       os.system('cls')
                       # 輸入新聞名. 獲取user_id, 打印t_type, 設置多項參數
                       title = input('\n\t新聞標題；')
                       user_id = __user_service.search_user_id(username)
                       type = __type_service.search_all_type()
                       for index in range(len(type)):
                           one = type[index]
                           print(Fore.LIGHTBLUE_EX,'\n\t{}.{}'.format(index+1, one[1]))
                       print(Style.RESET_ALL)
                       opt = input('\n\t類型編號；')
                       type_id = type[int(opt) - 1][0]
                       # TODO 新聞正文內容
                       path = input('\n\t請輸入文件路徑：')
                       file = open(path, 'r', encoding='utf-8')
                       content = file.read()
                       file.close()
                       is_top = input('\n\t置頂級別(0-5)：')
                       is_commit = input('\n\t是否提交(Y/N):')
                       if is_commit == 'Y' or is_commit == 'y':
                           __news_service.insert(title, user_id, type_id, content, is_top)
                           print('\n\t保存成功(3秒後自動返回)')
                           time.sleep(3)
                   elif choice == '2':
                       page = 1  # 必需要將變量設在循環外部, 否則每一次循環, 上一次搜索到的頁數將消失
                       while True:
                           os.system('cls')
                           count_page = __news_service.search_count_page()  # 查詢總頁數
                           result = __news_service.search_list(page)  # 所有紀錄的結果
                           # page 為當前頁數, 默認為第一頁
                           # 為何要使用索引的序號, 而不是主鍵值? 使新聞被刪除後, 不會主鍵顯示不連續
                           for index in range(len(result)):
                               one = result[index]  # 需要逐一提取數據 -主鍵, title, content_id, type_id
                               print(Fore.LIGHTBLUE_EX, '\n\t%d\t%s\t%s\t%s' % (index + 1, one[1], one[2], one[3]))
                           print(Fore.LIGHTBLUE_EX, '-----------------------------')
                           print('\n\t%d/%d' % (page, count_page))
                           print(Fore.LIGHTBLUE_EX, '-----------------------------')
                           print(Fore.LIGHTRED_EX, "\n\tback.返回上一層")
                           print(Fore.LIGHTRED_EX, "\n\tprev.上一頁")
                           print(Fore.LIGHTRED_EX, "\n\tnext.下一頁")
                           print(Style.RESET_ALL)
                           opt = input('\n\t請輸入操作編號：')
                           if opt == 'back':
                               break
                           elif opt == 'prev' and page > 1:
                               page -= 1  # 需不需要重新調用查詢功能? 不用! 因為page會保存在循環內, 到時會重新執行
                           elif opt == 'next' and page < count_page:  # 當前頁數 < 總頁數
                               page += 1
                           elif int(opt) >= 1 and int(opt) <= 10:  # 此處的opt要輸入控制台顯示的新聞序號, 一頁10條紀錄
                               # 但螢幕上看到的opt非原本的主鍵值, result[0]為原本結果的第一條紀錄
                               os.system('cls')  # 在提示信息前, 清理屏幕
                               news_id = result[int(opt) - 1][0]
                               result = __news_service.search_by_id(news_id)
                               title = result[0]
                               type = result[1]
                               is_top = result[2]
                               print('\n\t新聞原標題：%s' % (title))
                               new_title = input('\n\t新標題：')
                               print('\n\t原類型：%s' % (type))
                               # 打印類型列表
                               type = __type_service.search_all_type()
                               for index in range(len(type)):
                                   one = type[index]
                                   print(Fore.LIGHTBLUE_EX, '\n\t{}.{}'.format(index + 1, one[1]))
                               print(Style.RESET_ALL)
                               opt = input('\n\t類型編號；')
                               type_id = type[int(opt) - 1][0]
                               # TODO: 輸入新聞內容
                               path = input('\n\t輸入新聞內容路徑：')
                               file = open(path, 'r', encoding='utf-8')
                               content = file.read()
                               file.close()
                               print('\n\t原置頂級別：%s' % (is_top))
                               new_is_top = input('\n\t新置頂級別(0-5)：')
                               is_commit = input('\n\t是否提交?(Y/N)：')
                               if is_commit == 'Y' or is_commit == 'y':
                                   __news_service.update(news_id, new_title, type_id, content, new_is_top)
                                   print('修改成功(3秒自動返回)')
                                   time.sleep(3)
                   elif choice == 'back':
                       break
                   elif choice == 'exit':
                       sys.exit(0)
               elif role == '管理員':
                   print(Fore.LIGHTBLUE_EX, '\n\t1.新聞管理')
                   print(Fore.LIGHTBLUE_EX, '\n\t2.用戶管理')
                   print(Fore.LIGHTGREEN_EX, "\n\tback.退出登錄")
                   print(Fore.LIGHTGREEN_EX, "\n\texit.退出系統")
                   print(Style.RESET_ALL)
                   choice = input('\n\t輸入操作編號：')
                   if choice == '1':
                       while True: # 三級菜單, 一樣需要死循環
                           os.system('cls')
                           print(Fore.LIGHTBLUE_EX, '\n\t1.審核新聞')
                           print(Fore.LIGHTBLUE_EX, '\n\t2.刪除新聞')
                           print(Fore.LIGHTGREEN_EX, "\n\tback.返回上一層")
                           print(Style.RESET_ALL)  # 此使input顯示之語句為預設顏色
                           opt = input('\n\t請輸入操作編號：')
                           if opt == '1':
                               page = 1  # 必需要將變量設在循環外部, 否則每一次循環, 上一次搜索到的頁數將消失
                               while True:
                                   os.system('cls')
                                   count_page = __news_service.search_unreviewed_count_page()  # 查詢總頁數
                                   result = __news_service.search_unreviewed_list(page)  # 所有紀錄的結果
                                   # page 為當前頁數, 默認為第一頁
                                   # 為何要使用索引的序號, 而不是主鍵值? 使新聞被刪除後, 不會主鍵顯示不連續
                                   for index in range(len(result)):
                                       one = result[index]  # 需要逐一提取數據 -主鍵, title, content_id, type_id
                                       print(Fore.LIGHTBLUE_EX, '\n\t%d\t%s\t%s\t%s' % (index+1, one[1], one[2], one[3]))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print('\n\t%d/%d' % (page, count_page))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print(Fore.LIGHTRED_EX, "\n\tback.返回上一層")
                                   print(Fore.LIGHTRED_EX, "\n\tprev.上一頁")
                                   print(Fore.LIGHTRED_EX, "\n\tnext.下一頁")
                                   print(Style.RESET_ALL)
                                   opt = input('\n\t請輸入操作編號：')
                                   if opt == 'back':
                                       break
                                   elif opt == 'prev' and page > 1:
                                       page -= 1  # 需不需要重新調用查詢功能? 不用! 因為page會保存在循環內, 到時會重新執行
                                   elif opt == 'next' and page < count_page:  # 當前頁數 < 總頁數
                                       page += 1
                                   elif int(opt) >= 1 and int(opt) <= 10:  # 此處的opt要輸入控制台顯示的新聞序號, 一頁10條紀錄
                                       # 但螢幕上看到的opt非原本的主鍵值, result[0]為原本結果的第一條紀錄
                                       news_id = result[int(opt)-1][0]
                                       __news_service.update_unreviewed_news(news_id)
                                       result = __news_service.search_cache(news_id)  # 審核通過後, 緩存到redis數據
                                       title = result[0]
                                       username = result[3]
                                       type = result[2]
                                       content_id = result[1]
                                       # TODO: 查找新聞正文
                                       content = __news_service.search_content_by_id(content_id)
                                       is_top = result[4]
                                       create_time = str(result[5])  # 日期類型 -> redis只能保存str, int -> 強制轉換類型
                                       __news_service.cache_news(news_id, title, username, type, content, is_top, create_time)
                           elif opt == '2':
                               page = 1  # 必需要將變量設在循環外部, 否則每一次循環, 上一次搜索到的頁數將消失
                               while True:
                                   os.system('cls')
                                   count_page = __news_service.search_count_page()  # 查詢總頁數
                                   result = __news_service.search_list(page)  # 所有紀錄的結果
                                   # page 為當前頁數, 默認為第一頁
                                   # 為何要使用索引的序號, 而不是主鍵值? 使新聞被刪除後, 不會主鍵顯示不連續
                                   for index in range(len(result)):
                                       one = result[index]  # 需要逐一提取數據 -主鍵, title, content_id, type_id
                                       print(Fore.LIGHTBLUE_EX, '\n\t%d\t%s\t%s\t%s' % (index+1, one[1], one[2], one[3]))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print('\n\t%d/%d' % (page, count_page))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print(Fore.LIGHTRED_EX, "\n\tback.返回上一層")
                                   print(Fore.LIGHTRED_EX, "\n\tprev.上一頁")
                                   print(Fore.LIGHTRED_EX, "\n\tnext.下一頁")
                                   print(Style.RESET_ALL)
                                   opt = input('\n\t請輸入操作編號：')
                                   if opt == 'back':
                                       break
                                   elif opt == 'prev' and page > 1:
                                       page -= 1  # 需不需要重新調用查詢功能? 不用! 因為page會保存在循環內, 到時會重新執行
                                   elif opt == 'next' and page < count_page:  # 當前頁數 < 總頁數
                                       page += 1
                                   elif int(opt) >= 1 and int(opt) <= 10:  # 此處的opt要輸入控制台顯示的新聞序號, 一頁10條紀錄
                                       # 但螢幕上看到的opt非原本的主鍵值, result[0]為原本結果的第一條紀錄
                                       news_id = result[int(opt)-1][0]
                                       __news_service.delete_by_id(news_id)  # delete_by_id -> 刪除mongodb, mysql紀錄
                                       __news_service.delete_cache(news_id)  # news_id: redis內的主鍵
                           elif opt == 'back':
                               break
                   # 用戶管理
                   elif choice == '2':
                       while True:  # 死循環
                           os.system('cls')
                           # 新功能添加順序：dao -> service -> app
                           #　與用戶相關功能： user
                           print(Fore.LIGHTBLUE_EX, '\n\t1.添加用戶')
                           print(Fore.LIGHTBLUE_EX, '\n\t2.修改用戶')
                           print(Fore.LIGHTBLUE_EX, '\n\t3.刪除用戶')
                           print(Fore.LIGHTGREEN_EX, "\n\tback.返回上一層")
                           print(Style.RESET_ALL)  # 此使input顯示之語句為預設顏色
                           opt = input('\n\t請輸入操作編號：')
                           if opt == 'back':
                               break
                           elif opt == '1':
                               os.system('cls')
                               # 確認添加用戶身分 -創建名字和郵箱
                               username = input('\n\t用戶名：')
                               password = getpass('\n\t密碼：')
                               repassword = getpass('\n\t重複密碼：')
                               if password != repassword:
                                   # 用戶提示
                                   print('\n\t兩次密碼不一致(3秒後自動返回)')
                                   time.sleep(3)
                                   continue
                               email = input('\n\t郵箱：')
                               # 先打印數據庫現存資料
                               result = __role_service.search_list()
                               for index in range(len(result)):
                                   one = result[index] # 使序號連續
                                   print(Fore.LIGHTBLUE_EX, '%d.%s' % (index+1, one[1]))
                               print(Style.RESET_ALL)
                               opt = input('\n\t角色編號；')
                               role_id = result[int(opt)-1][0]
                               # 調用添加用戶
                               __user_service.insert(username, password, email, role_id)
                               # 用戶提示
                               print('\n\t保存成功(3秒後自動返回)')
                               time.sleep(3)
                           elif opt == '2':
                               page = 1  # 必需要將變量設在循環外部, 否則每一次循環, 上一次搜索到的頁數將消失
                               while True:
                                   os.system('cls')
                                   count_page = __user_service.search_count_page()  # 查詢總頁數
                                   result = __user_service.search_list(page)  # 所有紀錄的結果
                                   for index in range(len(result)):
                                       one = result[index]  # 需要逐一提取數據 -主鍵, title, content_id, type_id
                                       print(Fore.LIGHTBLUE_EX,
                                             '\n\t%d\t%s\t%s' % (index + 1, one[1], one[2]))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print('\n\t%d/%d' % (page, count_page))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print(Fore.LIGHTRED_EX, "\n\tback.返回上一層")
                                   print(Fore.LIGHTRED_EX, "\n\tprev.上一頁")
                                   print(Fore.LIGHTRED_EX, "\n\tnext.下一頁")
                                   print(Style.RESET_ALL)
                                   opt = input('\n\t請輸入操作編號：')
                                   if opt == 'back':
                                       break
                                   elif opt == 'prev' and page > 1:
                                       page -= 1  # 需不需要重新調用查詢功能? 不用! 因為page會保存在循環內, 到時會重新執行
                                   elif opt == 'next' and page < count_page:  # 當前頁數 < 總頁數
                                       page += 1
                                   elif int(opt) >= 1 and int(opt) <= 10:  # 此處的opt要輸入控制台顯示的新聞序號, 一頁10條紀錄
                                       os.system('cls')
                                       user_id = result[int(opt) - 1][0]
                                       username = input('\n\t新用戶名：')
                                       password = getpass('\n\t密碼：')
                                       repassword = getpass('\n\t重複密碼：')
                                       if password != repassword:
                                           # 用戶提示
                                           print(Fore.LIGHTRED_EX, '\n\t兩次密碼不一致(3秒後自動返回)')
                                           print(Style.RESET_ALL)
                                           time.sleep(3)
                                           break  # 結束這次判斷
                                       result = __role_service.search_list()
                                       email = input('\n\t請輸入新郵箱：')
                                       for index in range(len(result)):
                                           one = result[index]  # 使序號連續
                                           print(Fore.LIGHTBLUE_EX, '%d.%s' % (index + 1, one[1]))
                                       print(Style.RESET_ALL)
                                       opt = input('\n\t角色編號；')
                                       role_id = result[int(opt)-1][0]
                                       opt = input('\n\t是否保存(Y/N)：')
                                       if opt == 'Y' or opt == 'y':
                                           __user_service.update(id, username, password, email, role_id)
                                           print('\n\t保存成功(3秒後自動返回)')
                                           time.sleep(3)
                                   # 报错原因为输入的opt不满足等于“back”、“prev”、“next”等条件且无法转为数字类型而报错
                                   elif not opt.isdigit():
                                       print('輸入錯誤')
                           elif opt == '3':
                               page = 1  # 必需要將變量設在循環外部, 否則每一次循環, 上一次搜索到的頁數將消失
                               while True:
                                   os.system('cls')
                                   count_page = __user_service.search_count_page()  # 查詢總頁數
                                   result = __user_service.search_list(page)  # 所有紀錄的結果
                                   # page 為當前頁數, 默認為第一頁
                                   # 為何要使用索引的序號, 而不是主鍵值? 使新聞被刪除後, 不會主鍵顯示不連續
                                   for index in range(len(result)):
                                       one = result[index]  # 需要逐一提取數據 -主鍵, title, content_id, type_id
                                       print(Fore.LIGHTBLUE_EX,
                                             '\n\t%d\t%s\t%s' % (index + 1, one[1], one[2]))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print('\n\t%d/%d' % (page, count_page))
                                   print(Fore.LIGHTBLUE_EX, '-----------------------------')
                                   print(Fore.LIGHTRED_EX, "\n\tback.返回上一層")
                                   print(Fore.LIGHTRED_EX, "\n\tprev.上一頁")
                                   print(Fore.LIGHTRED_EX, "\n\tnext.下一頁")
                                   print(Style.RESET_ALL)
                                   opt = input('\n\t請輸入操作編號：')
                                   if opt == 'back':
                                       break
                                   elif opt == 'prev' and page > 1:
                                       page -= 1  # 需不需要重新調用查詢功能? 不用! 因為page會保存在循環內, 到時會重新執行
                                   elif opt == 'next' and page < count_page:  # 當前頁數 < 總頁數
                                       page += 1
                                   elif int(opt) >= 1 and int(opt) <= 10:  # 此處的opt要輸入控制台顯示的新聞序號, 一頁10條紀錄
                                       os.system('cls')
                                       user_id = result[int(opt)-1][0]
                                       __user_service.delete_by_id(user_id)
                                       print('\n\t刪除成功(3秒後自動返回)')
                                       time.sleep(3)

                       # 二級菜單退出
                   elif choice == 'back':
                       break
                   elif choice == 'exit':
                       sys.exit(0)
       else:
           print('\n\t登陸失敗(3秒後自動返回)')
           time.sleep(3)
    elif opt == '2':
       sys.exit(0)

