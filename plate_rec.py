import sys
import requests
from pprint import pprint

BASE_URL = 'https://platerecognizer.com/v1/plate-reader'


def plate_recog(file):
    file = 'Screenshot 2019-03-30 at 15.36.06.png'

    try:
        if sys.argv[1]:
            file = sys.argv[1]
            print(file)
    except IndexError:
        pass

    with open(file, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token 95520c18606dcc83abe1793a712643f6793daace'})
    # pprint(response.json())
    pprint(response.json()['results'][0]['plate'])


if __name__ == '__main__':
    plate_recog('Screenshot 2019-03-30 at 15.36.06.png')
