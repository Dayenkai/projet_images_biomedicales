# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:10:14 2020

@author: beker
"""

import numpy as np
import cv2 as cv

def segment_the_bail(image):
    
    image = cv.GaussianBlur(image, (5, 5), 10)
    threshold_left = 100 - np.mean(image)
    image_seg = image > np.mean(image) + threshold_left
    return image_seg