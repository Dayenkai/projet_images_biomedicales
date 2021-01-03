# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:48:14 2021

@author: beker
"""

import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage import io

import cv2 as cv

# Test scipy version, since active contour is only possible
# with recent scipy version

def snake_segmentation(image):

    spaced_numbers = np.linspace(0, 2*np.pi, 400)
    abcisse = 60 + 60*np.cos(spaced_numbers)
    ordonnee = 120 + 60*np.sin(spaced_numbers)
    init_array = np.array([abcisse, ordonnee]).T


    snakeman = active_contour(gaussian(image, 3),
                           init_array, alpha=0.015, beta=10, gamma=0.001)

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    plt.gray()
    ax.imshow(image)
    #ax.plot(init_array[:, 0], init_array[:, 1], '--r', lw=3)
    ax.plot(snakeman[:, 0], snakeman[:, 1], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, image.shape[1], image.shape[0], 0])
    
    
img = io.imread('C:\\Users\\beker\\Desktop\\training_sa_crop_pat0\\training_sa_crop_pat00075.bmp')
snake_segmentation(img)
