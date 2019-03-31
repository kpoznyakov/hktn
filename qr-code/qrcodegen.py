# coding = "utf-8"
"""
сервис для кодировки ID в qr-code и его занесение в базу данных
ID = ID-пользователя/utime/[0/1]-одноразовый/многоразовый
:param: user_ID, usability, email
:return: qr-code send by e-mail
"""


import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from random import randint
from time import time

import psycopg2
import qrcode


def generate(user_id, usability, email='desciuerant@ya.ru'):
    data = str(user_id) + str(time()) + str(usability)

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
    memf = BytesIO()
    img.save(memf, format='png')
    memf.seek(0)
    eimg = memf.read()
    eimg = MIMEImage(eimg)

    HOST = 'smtp.gmail.com'
    FROM = 'test.guestsystem'
    PASSWORD = 'gAaFH4X5V74grLz'
    TO = email
    SUBJECT = 'Be our guest!'

    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT
    msg.attach(eimg)

    with smtplib.SMTP(HOST, 587) as s:
        s.starttls()
        s.login(FROM, PASSWORD)
        s.send_message(msg)
