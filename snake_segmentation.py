# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:13:44 2020

@author: beker
"""

from skimage import data
import numpy as np
import matplotlib.pyplot as plt
from skimage import io

import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
from skimage.morphology import disk
from skimage.filters import rank


images = io.ImageCollection('.\\images\\RawData\\Training Dataset\\training_sa_crop_pat0')
single_image = io.imread('.\\images\\RawData\\Training Dataset\\training_sa_crop_pat0\\training_sa_crop_pat00100.bmp')
image_gray = color.rgb2gray(single_image)

print('Type:', type(images))
images.files

def image_show(image, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    return fig, ax

#♠image_show(text < text_threshold);


fig, ax = plt.subplots(1, 1)
ax.hist(single_image.ravel(), bins=32, range=[0, 256])
ax.set_xlim(0, 256);
selem = disk(20)

print(np.mean(single_image))


def circle_points(resolution, center, radius):
    
    radians = np.linspace(0, 2*np.pi, resolution)
    
    c = center[1] + radius*np.cos(radians)#polar co-ordinates
    r = center[0] + radius*np.sin(radians)

    return np.array([c, r]).T



points = circle_points(150, [100, 63], (np.mean(single_image) * 90) / 65.77 )[:-1]

print(points)

snake = seg.active_contour(image_gray, points, alpha=0.05)

fig, ax = image_show(image_gray)
ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)