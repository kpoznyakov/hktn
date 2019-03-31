# coding = "utf-8"
"""
сервис для кодировки ID в qr-code и его занесение в базу данных
- ID = ID-пользователя/utime/[0/1]-одноразовый/многоразовый
:param: ID строка
:return: qr-code
"""

# TODO
# ! поменять usability на данные с сайта
# * отправлять .png обратно на сайт

from random import randint
from time import time

import psycopg2
import qrcode


def data_encoding(user_id, usability):
    return str(user_id) + str(time()) + str(usability)


conn = psycopg2.connect(user='postgres', password='qweasdzxc',
                        database='entrance', host='100.100.148.215')
cursor = conn.cursor()
cursor.execute('SELECT id from entrance.dbo.user')
user_id = cursor.fetchone()[0]
cursor.close()
conn.close()

usability = 0
data = data_encoding(user_id, usability)

conn = psycopg2.connect(user='postgres', password='qweasdzxc',
                        database='app', host='100.100.148.215')
cursor = conn.cursor()
cursor.execute("SELECT app.dbo.insert_QR('{}', {})".format(data, user_id))
conn.commit()
cursor.close()
conn.close()

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image()

img.save('guestcode.png')
