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
import snake_segmentation as ss
import edge_segmentation as es

image = color.rgb2gray(io.imread('testing.png'))
areas = aire.getAreas(image)

plt.figure(1)
plt.imshow(image)
plt.figure(2)
plt.imshow(areas)
plt.show()
input("waiting...")
plt.close()