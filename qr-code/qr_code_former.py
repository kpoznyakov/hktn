# coding = "utf-8"
""" TODO
сервис для кодировки ID в qr-code и его занесение в базу
данных
"""


import qrcode

qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)

data = "Hello, duda"

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image()

img.save("image.png")
# img.save("image.bmp")
# img.save("image.jpeg")
# img.save("image.jpg")
