# from PIL import Image

# Img = Image.open("/Users/hexk0131/Downloads/unsamples-2/OwVOoS8Dmv0.jpg")

# rotated = Img.rotate(45)

# rotated.show()

import cv2
from matplotlib import pyplot as plt
img = cv2.imread('./5.png',0)
hist1 = cv2.calcHist([img],[0],None,[256],[0,256])

plt.subplot(221),plt.imshow(img,'gray'),plt.title('Red Line')
plt.subplot(222),plt.plot(hist1,color='r')
plt.xlim([0,256]) 
plt.show()