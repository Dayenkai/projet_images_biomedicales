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

import aire

image1 = io.imread("images\\resultats\\region_seg\\original\\p2\\savedImage2133.bmp")
result = aire.getAreas(image1, True)
image2 = result[0]

plt.figure(1)
plt.imshow(image1)
plt.figure(2)
plt.imshow(image2)
plt.show()
print(result[1])
input("waiting...")
plt.close()