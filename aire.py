# -*- coding: utf-8 -*-
"""
Created on Tue Dec  19 02:07:08 2020

@author: theo
"""

import itertools
import operator
import matplotlib
matplotlib.rcParams['interactive'] == True
matplotlib.interactive(True)
from matplotlib import pyplot as plt
from skimage import color
from skimage import io
import numpy as np
import re
import csv
import os

def __listsCommon(list1, list2) :
    """Returns True if 'list1' and 'list2' have at least 1 element in common, False otherwise
    list1 : 1D int list
    list2 : 1D int list
    """
    for i in range(len(list1)) :
        for j in range(len(list2)) :
            if (list1[i]==list2[j]) :
                return True
    return False

def __unlinkedJoints(theList) :
    """Returns True if 'theList' contains lists that have at least 1 element in common
    theList : 2D list of 1D int list
    """
    for i in range(len(theList)) :
        for j in range(i+1, len(theList)) :
            if (__listsCommon(theList[i], theList[j])) :
                return True
    return False

def getAreas(image, hard) :
    """Returns a tuple of 2 elements:
        1: 2D list of 'image', but with 1 color per connected area
        2: list different areas sorted biggest to smallest
    image : 2D list of greyscale image
    hard : boolean that governs how areas are sperated
    """
    height = image.shape[0]
    width = image.shape[1]
    areas = [[0 for i in range(width)] for i in range(height)]
    color = 0
    jointures = []
    dictionnary = {}

    # goes through the image left to right, top to bottom,
    # and joins pixels that are connected to the top or to the left
    print(" 'getAreas': 1/4")
    for i in range(1, height-1) :
        for j in range(1, width-1) :
            if image[i][j] :
                currentColor = color
                if (areas[i-1][j-1]) :
                    currentColor = areas[i-1][j-1]
                elif (areas[i-1][j]) :
                    currentColor = areas[i-1][j]
                elif (areas[i-1][j+1]) :
                    currentColor = areas[i-1][j+1]
                elif (areas[i][j-1]) :
                    currentColor = areas[i][j-1]
                else :
                    color +=1
                    currentColor = color
                areas[i][j] = currentColor

    # fetch the joints between areas that should be connected
    print(" 'getAreas': 2/4")
    for i in range(1, height-1) :
        for j in range(1, width-1) :
            if (areas[i][j]) :
                tmp = [areas[i][j]]
                if (areas[i-1][j]) :
                    tmp.append(areas[i-1][j])
                if (areas[i][j-1]) :
                    tmp.append(areas[i][j-1])
                if (areas[i][j+1]) :
                    tmp.append(areas[i][j+1])
                if (areas[i+1][j]) :
                    tmp.append(areas[i+1][j])
                if (not hard) :
                    if (areas[i-1][j-1]) :
                        tmp.append(areas[i-1][j-1])
                    if (areas[i-1][j+1]) :
                        tmp.append(areas[i-1][j+1])
                    if (areas[i+1][j-1]) :
                        tmp.append(areas[i+1][j-1])
                    if (areas[i+1][j+1]) :
                        tmp.append(areas[i+1][j+1])

                tmp.sort()
                tmp = list(set(tmp))
                jointures.append(tmp)
    jointures.sort()
    jointures = list(jointures for jointures,_ in itertools.groupby(jointures))

    # create a list of list of colors that should be the same
    
    print(" 'getAreas': 3/4")
    while True :
        i=0
        end=len(jointures)
        while (i < end) :
            j=i+1
            while (j < end) :
                if __listsCommon(jointures[i], jointures[j]) :
                    jointures[i] = list(set(jointures[i]).union(jointures[j]))
                    jointures[i].sort()
                    jointures.pop(j)
                    end-=1
                else :
                    j+=1
            i+=1
        if not (__unlinkedJoints(jointures)) :
            break

    print(" 'getAreas': 4/4")
    for i in range(height) :
        for j in range(width) :
            # change the color of connected areas to the same one
            for k in range(len(jointures)) :
                if (areas[i][j] in jointures[k]) :
                    areas[i][j] = k+1
            # add pixel to area density
            if (areas[i][j]) :
                if (areas[i][j] in dictionnary.keys()) :
                    dictionnary[areas[i][j]] += 1
                else :
                    dictionnary[areas[i][j]] = 1
    dictionnary = dict(sorted(dictionnary.items(), key=operator.itemgetter(1),reverse=True))

    return(areas, dictionnary)

def areasImagesForGroundTruth() :
    images_list = io.imread_collection('working_images\\*.bmp', conserve_memory=True)
    for cpt in range(len(images_list)):
        print("image: "+str(cpt+1)+"/"+str(len(images_list)))
        image = images_list[cpt]
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if (image[i][j]<200) :
                    image[i][j] = 0
                else :
                    image[i][j] = 1

        areas = getAreas(image, True)
        filename = 'images\\resultats\\ground_truth_area\\gtximg'+str(cpt)+'.bmp'
        io.imsave(filename, np.asarray(areas[0]))

def areasImagesForRegionSegmentation() :
    images_list = io.imread_collection('images\\resultats\\snake_seg\\modified\\*.bmp', conserve_memory=True)
    for cpt in range(len(images_list)):
        print("image: "+str(cpt+1)+"/"+str(len(images_list)))
        image = color.rgb2gray(images_list[cpt])

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if (image[i][j]>0) :
                    image[i][j] = 1
                else :
                    image[i][j] = 0

        areas = getAreas(image, True)
        filename = 'images\\resultats\\snake_seg_area\\rgximg'+str(cpt)+'.bmp'
        io.imsave(filename, np.asarray(areas[0]))

def writeCSV() :
    path = "images\\resultats\\snake_seg_area"
    table = []
    images_list = io.imread_collection(str(path+"\\*.bmp"), conserve_memory=True)
    files = os.listdir(path)
    for i in range(len(images_list)):
        print(str(files[i])+": "+str(i+1)+"/"+str(len(images_list)))        
        image = color.rgb2gray(images_list[i])
        values = list(getAreas(image, True)[1].values())[:2]
        line = [files[i]]
        for v in values:
            line.append(v)
        table.append(line)
    with open(path+"\\output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(table)
    
#areasImagesForRegionSegmentation()
writeCSV()

"""
input("waiting...")
plt.close()
"""