import random
import sys
import requests
# from pprint import pprint
from time import sleep


def check_is_car():
    while True:
        sleep(5)
        return random.choice([0, 1])


BASE_URL = 'https://platerecognizer.com/v1/plate-reader'


def plate_recog(file):
    try:
        if sys.argv[1]:
            file = sys.argv[1]
            print(file)
    except IndexError:
        pass

    with open(file, 'rb') as fp:
        response = requests.post(
            BASE_URL,
            files=dict(upload=fp),
            headers={'Authorization': 'Token 95520c18606dcc83abe1793a712643f6793daace'})
    # pprint(response.json())
    print(response.json()['results'][0]['plate'])


if __name__ == '__main__':
    if check_is_car():
        plate_recog('../Screenshot 2019-03-30 at 15.36.06.png')
