from PIL import Image

Img = Image.open("/Users/hexk0131/Downloads/unsamples-2/OwVOoS8Dmv0.jpg")

rotated = Img.rotate(45)

rotated.show()