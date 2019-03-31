import os
import random
from time import sleep

import psycopg2
import requests

params = {
    'dbname': 'parking',
    'user': 'postgres',
    'password': 'qweasdzxc',
    'host': '100.100.148.215',
    'port': 5432
}


def search_plate(plate):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("SELECT dbo.check_car(%s, %s)", (plate, 1))
    # print(cur.fetchone())
    # print('dfdfd')
    if cur.fetchone()[0] == 1:
        conn.commit()
        cur.close()
        conn.close()
        return True
    conn.commit()
    cur.close()
    conn.close()
    return False


def log_plate(plate):
    pass


def check_is_car():
    while True:
        sleep(3)
        is_car = random.choice([0, 1])
        if is_car:
            print('Подъехал автомобиль. Номер:')
            return is_car


def plate_recog(dir_, file):
    base_url = 'https://platerecognizer.com/v1/plate-reader'
    with open(dir_ + file, 'rb') as fp:
        response = requests.post(
            base_url,
            files=dict(upload=fp),
            headers={'Authorization': 'Token 95520c18606dcc83abe1793a712643f6793daace'})
    try:
        res = response.json()['results'][0]['plate']
        print(res)
        if search_plate(res):
            print('Проезжайте!')
        else:
            print('Номер не найден. Обратитесь на пункт охраны или воспользуйтесь картой доступа.')
    except IndexError:
        print(response.text)
        print('Не распознан. Воспользуйтесь пропуском.')
        pass


def select_random_file(dir_):
    plate_files = []
    for root, dirs, files in os.walk(dir_):
        for file in files:
            plate_files.append(file)
        random_img = random.choice(plate_files)
        return random_img


if __name__ == '__main__':
    # while True:
    #     search_plate('r001am77')
    #     sleep(3)
    dir_with_plates = './plates_img/'
    while True:
        if check_is_car():
            foo = select_random_file(dir_with_plates)
            plate_recog(dir_with_plates, foo)
