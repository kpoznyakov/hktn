# coding = "utf-8"
""" TODO
сервис для декодировки ID в qr-code и его проверка в базе
данных на подлинность
"""

import qrdecode

qr = qrdecode.decode('image.png')
print(qr)
