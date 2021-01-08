# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:41:57 2021

@author: beker
"""
import numpy as np
import cv2
import numpy as np

img = cv2.imread('C:\\Users\\beker\\Desktop\\training_sa_crop_pat0\\Itraining_8170.bmp', cv2.IMREAD_COLOR)


#convert img to grey
img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

image_binary = np.zeros((img.shape[1],
                         img.shape[0], 1),
                        np.uint8)


r_mask = np.zeros_like(img, dtype='bool')
#set a thresh
thresh = 70

kernel = np.ones((2,2),np.uint8)

image = cv2.GaussianBlur(img_grey, (5, 5), 1)
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel,iterations = 1)
erosion = cv2.erode(image,kernel,iterations = 2)
image = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel,iterations = 5)
image = cv2.erode(image,kernel,iterations = 1)


#get threshold image
ret,thresh_img = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
#find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#create an empty image for contours
img_contours = np.zeros(img.shape)
# draw the contours on the empty image
cv2.drawContours(img, contours, -1, (255, 255, 255), -1)

cv2.imshow("bruh",img)
#save image
cv2.imwrite('D:/Resultats_Ventricules/Itraining_8170.bmp',img) 