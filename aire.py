import matplotlib
matplotlib.rcParams['interactive'] == True
matplotlib.interactive(True)
from matplotlib import pyplot as plt
from skimage import color
from skimage import io
import itertools

def listsCommon(list1, list2) :
    """Returns True if 'list1' and 'list2' have at least 1 element in common, False otherwise
    list1 : 1D int list
    list2 : 1D int list
    """
    for i in range(len(list1)) :
        for j in range(len(list2)) :
            if (list1[i]==list2[j]) :
                return True
    return False

def unlinkedJoints(theList) :
    """Returns True if 'theList' contains lists that have at least 1 element in common
    theList : 2D list of 1D int list
    """
    for i in range(len(theList)) :
        for j in range(i+1, len(theList)) :
            if (listsCommon(theList[i], theList[j])) :
                return True
    return False

def getAreas(image) :
    """Returns 'image', but with 1 color per connected area
    image : 2D list of greyscale image
    """
    height = image.shape[0]
    width = image.shape[1]
    areas = [[0 for i in range(width)] for i in range(height)]
    color = 0
    jointures = []

    # goes through the image left to right, top to bottom,
    # and joins pixels that are connected to the top or to the left
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
    for i in range(1, height-1) :
        for j in range(1, width-1) :
            if (areas[i][j]) :
                tmp = [areas[i][j]]
                if (areas[i-1][j-1]) :
                    tmp.append(areas[i-1][j-1])
                if (areas[i-1][j]) :
                    tmp.append(areas[i-1][j])
                if (areas[i-1][j+1]) :
                    tmp.append(areas[i-1][j+1])
                if (areas[i][j-1]) :
                    tmp.append(areas[i][j-1])
                if (areas[i][j+1]) :
                    tmp.append(areas[i][j+1])
                if (areas[i+1][j-1]) :
                    tmp.append(areas[i+1][j-1])
                if (areas[i+1][j]) :
                    tmp.append(areas[i+1][j])
                if (areas[i+1][j+1]) :
                    tmp.append(areas[i+1][j+1])
                tmp.sort()
                tmp = list(set(tmp))
                jointures.append(tmp)
    jointures.sort()
    jointures = list(jointures for jointures,_ in itertools.groupby(jointures))

    # create a list of list of colors that should be the same
    while True :
        i=0
        end=len(jointures)
        while (i < end) :
            j=i+1
            while (j < end) :
                if listsCommon(jointures[i], jointures[j]) :
                    jointures[i] = list(set(jointures[i]).union(jointures[j]))
                    jointures[i].sort()
                    jointures.pop(j)
                    end-=1
                else :
                    j+=1
            i+=1
        if not (unlinkedJoints(jointures)) :
            break

    # change the color of connected areas to the same one
    for i in range(height) :
        for j in range(width) :
            for k in range(len(jointures)) :
                if (areas[i][j] in jointures[k]) :
                    areas[i][j] = k+1

    return(areas)

image = color.rgb2gray(io.imread('testing.png'))
areas = getAreas(image)

plt.figure(1)
plt.imshow(image)
plt.figure(2)
plt.imshow(areas)
plt.show()
input("waiting...")
plt.close()
