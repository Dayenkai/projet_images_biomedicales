# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:47:15 2021

@author: beker
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import cv2
import scipy.ndimage as ndimage  


def snake_segmentation(image):

    #On récupère une valeur de seuil restante pour l'image 
    #(On a estimé que le seuillage approprié pour l'ensemble des images environnait la valeur 100)
    threshold_left = 97 - np.mean(image)
     
    #On crée une figure et un ensemble de subplots
    fig, ax = plt.subplots()
    
    #On retourne un tableau d'une certaine forme rempli par la valeur '1'
    kernel = np.ones((2,2),np.uint8)
    
    #On applique ici plusieurs filtres sur l'image. Un filtre Gaussien et Une érosion et deux 'Closing' sont effectué.
    #closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel,iterations = 1)
    image = cv2.GaussianBlur(image, (5, 5), 8)    
    erosion = cv2.erode(image,kernel,iterations = 2)
    image = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel,iterations = 5)

    #Une moyenne de seuillage aux alentour de 100 a été déduit
    image = image > np.mean(image) + threshold_left

    # Trouve les contours à une valeur de 0.8, puis trie les contours de sorte à trouver les plus long
    contours = measure.find_contours(image, 0.9)
    contour = sorted(contours, key=lambda x: len(x))[-1]

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    plt.gray()
    ax.imshow(image)
    #ax.plot(init_array[:, 0], init_array[:, 1], '--r', lw=3)
    ax.plot(snakeman[:, 0], snakeman[:, 1], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, image.shape[1], image.shape[0], 0])

    return image
    # Crée un masque vide 
    r_mask = np.zeros_like(image, dtype='bool')
    
    # Créer un contour de l'image en utilisant les coordonnées des contours arrondi à l'int le plus proche
    r_mask[np.round(contour[:, 0]).astype('int'), np.round(contour[:, 1]).astype('int')] = 1
    
    # Rempli le masque par le contour récupéré
    r_mask = ndimage.binary_fill_holes(r_mask)
   
    return r_mask
