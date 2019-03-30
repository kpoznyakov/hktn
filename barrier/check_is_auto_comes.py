import random
import sys
import requests
import os
# from pprint import pprint
from time import sleep


def check_is_car():
    while True:
        sleep(3)
        return random.choice([0, 1])


BASE_URL = 'https://platerecognizer.com/v1/plate-reader'


def plate_recog(dir_, file):
    # print(file)

    with open(dir_ + file, 'rb') as fp:
        response = requests.post(
            BASE_URL,
            files=dict(upload=fp),
            headers={'Authorization': 'Token 95520c18606dcc83abe1793a712643f6793daace'})
    print(response.text)
    try:
        if response.json()['results'] is None:
            pass
        else:
            print(response.json()['results'][0]['plate'])
    except IndexError:
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
    # print(select_random_file('./plates_img/'))
    while True:
        if check_is_car():
            l = select_random_file('./plates_img/')
            plate_recog('./plates_img/', l)
