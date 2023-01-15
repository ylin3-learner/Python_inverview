# coding:utf-8

import mysql.connector.pooling
import os

__config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'tony1120',
    'database': 'vega',
    'auth_plugin': 'mysql_native_password'
}

try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        **__config,
        pool_size=10
    )
except Exception as e:
        print(e)



# 将图片提取为二进制数据并保存到mysql数据库里
class Dao:

    def read_image_dao(self, name):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'SELECT image FROM t_image WHERE name=%s'
            cursor.execute(sql, [name])
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            if 'con' in dir():
                print(e)
        finally:
            if 'con' in dir():
                con.close()

    def save_image_dao(self, name, image):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'INSERT INTO t_image(name, image) VALUES (%s, %s)'
            cursor.execute(sql, (name, image))
        except Exception as e:
            if 'con' in dir():
                print(e)
        finally:
            if 'con' in dir():
                con.close()

__dao = Dao()

def read_image(name, file_name, dir_path):
    path = os.path.join(dir_path, file_name)
    try:
        image = __dao.read_image_dao(name)
        with open(image, 'wb+') as f:
            f.write(image)
    except Exception as e:
        print(e)

def save_image(file_name, dir_path):
    path = os.path.join(file_name, dir_path)  # 將路徑導入此文件夾
    try:
        with open(path, 'rb') as f:
            image = f.read()
        result = __dao.save_image_dao(file_name, image)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    file_name = 'test.jpg'
    dir_path = os.getcwd()
    save_image(file_name, dir_path)
    new_file_name = 'test_new.jpg'
    read_image(file_name, new_file_name, dir_path)
