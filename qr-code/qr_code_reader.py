# coding = "utf-8"
"""
декодирование ID в qr-code и его проверка в базе данных на подлинность
:param: qr-code
:return: flag
flag - описывает прошла ли проверка в базе данных - открыть дверь
"""

import psycopg2
import qrdecode

qr = qrdecode.decode('guestcode.png')
conn = psycopg2.connect(user='postgres', password='qweasdzxc',
                        database='app', host='100.100.148.215')
cursor = conn.cursor()
cursor.execute("SELECT app.dbo.check_QR('{}')".format(qr))
conn.commit()
key = cursor.fetchone()[0]
cursor.close()
conn.close()
if key == 1:
    flag = True
else:
    flag = False
print(flag)
