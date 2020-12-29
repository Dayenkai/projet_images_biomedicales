# -*- coding: utf-8 -*-
"""
Created on Tue Dec  29 15:03:32 2020

@author: theo
"""

import matplotlib
matplotlib.rcParams['interactive'] == True
matplotlib.interactive(True)
from matplotlib import pyplot as plt
from skimage import color
from skimage import io

import aire
from snake_segmentation import segment_the_bail as snakeSeg
##import edge_segmentation as es

image = color.rgb2gray(io.imread('..\\test.bmp'))
seg = snakeSeg(image)
areas = aire.getAreas(seg, True)

plt.figure(1)
plt.imshow(seg)
plt.figure(2)
plt.imshow(areas[0])
plt.show()
print(areas[1])
input("waiting...")
plt.close()