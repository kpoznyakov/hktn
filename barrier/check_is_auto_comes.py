import random
import requests
import os
from time import sleep
import datetime


def check_is_car():
    while True:
        sleep(3)
        is_car = random.choice([0, 1])
        if is_car:
            print('Подъехал автомобиль. Номер:')
            return is_car


BASE_URL = 'https://platerecognizer.com/v1/plate-reader'


def plate_recog(dir_, file):
    # print(file)
    allowed_plates = [
        's001ss01',
        'r001am77',
        'm5550e61'
    ]
    with open(dir_ + file, 'rb') as fp:
        response = requests.post(
            BASE_URL,
            files=dict(upload=fp),
            headers={'Authorization': 'Token 95520c18606dcc83abe1793a712643f6793daace'})
    # print(response.text)
    try:
        if response.json()['results'] is None:
            print(response.text)
            pass
        else:
            res = response.json()['results'][0]['plate']
            # if (SELECT `status` FROM some WHERE plate = res) is 'Allow':
            #
            #
            print(res)
            if res in allowed_plates:
                print('Проезжайте!')
            else:
                print('Номер не найден. Обратитесь на пункт охраны или воспользуйтесь картой доступа.')
    except IndexError:
        print('Не распознан. Воспользуйтесь пропуском.')
        pass


def select_random_file(dir_):
    plate_files = []
    for root, dirs, files in os.walk(dir_):
        for file in files:
            plate_files.append(file)
            # print(plate_files)
        random_img = random.choice(plate_files)
        # print(random_img)
        return random_img


if __name__ == '__main__':
    dir_with_plates = './plates_img/'
    # print(select_random_file(dir_with_plates))
    while True:
        if check_is_car():
            l = select_random_file(dir_with_plates)
            plate_recog(dir_with_plates, l)
