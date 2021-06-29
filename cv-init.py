import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('C:/Users/12269/Downloads/opslevel/Screenshot_1.jpg',0)
img = cv.medianBlur(img,5)

th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
            
th3 = cv.GaussianBlur(th3,(5,5),0)

plt.imshow(th3,'gray')
plt.xticks([]),plt.yticks([])
plt.show()
