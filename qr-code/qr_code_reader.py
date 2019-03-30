# coding = "utf-8"
""" TODO
сервис для декодировки ID в qr-code и его проверка 
в базе данных на подлинность
"""

import psycopg2
import qrdecode

qr = qrdecode.decode('guestcode.png')
conn = psycopg2.connect(user='postgres', password='qweasdzxc',
                        database='app', host='100.100.148.215')
cursor = conn.cursor()
cursor.execute("SELECT app.dbo.check_QR('{}')".format(qr))
key = cursor.fetchone()
print(key)
