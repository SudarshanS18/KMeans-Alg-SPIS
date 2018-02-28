import math
import random
import pylab
import imageio
import os
import re
import csv
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

"""
    This class point is meant to represent a point, with coordinates x and y.
"""
class Point(object):
    def __init__(self, coords):

        #COORDS is list of coordinates
        self.coords = coords
        self.X = coords[0]
        self.Y = coords[1]

    def __repr__(self):
        return str(self.coords)
    
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

"""
    Cluster is an object representing the physical cluster that
    points are associated with. Each cluster has a center (centroid)
    and it has one main method, calculateCentroid, in which it can
    find it's own centroid.
"""
class Cluster(object):
    def __init__(self, points):
        
        #points is an array of points assigned to this centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        

    def calculateCentroid(self):

        #just define number of points
        numPoints = len(self.points)

        # just variables to store all x and y coords and sums of them to take average
        xCoords, yCoords = [],[]
        xSum, ySum = 0,0

        # loop through and find all the x and y coords of all the points.
        for p in self.points:
            xCoords.append(p.X)
            xSum += p.X
            yCoords.append(p.Y)
            ySum += p.Y

        # the centroid is a new point with the averages of all the points.
        centroid = Point([xSum/len(xCoords), ySum/len(yCoords)])
        return centroid


    def renew(self, newPoints):
        
        # store old centroid
        old_centroid = self.centroid

        # save the new points I just got
        self.points = newPoints

        # find the new centroid
        self.centroid = self.calculateCentroid()

        # return how much the centroid changed.
        change = getDistance(old_centroid, self.centroid)
        return change

    def __repr__(self):
        return str(self.points)
    
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

"""
    This will import a csv file with columns of latitude and longitude
    specified to import from.
"""
def importData(fileName, latLocation, longLocation):

    # Three arrays, one for title, one for x values, one for y values
    title, xVals, yVals = [], [], []

    #remove all the nulls and the other stuff
    cleanData(fileName, latLocation, longLocation)

    #now open up that new file
    with open(fileName) as csvfile:

        #ignore the header
        next(csvfile)

        #reader is going to read the csv file with commas as the separation
        reader = csv.reader(csvfile, delimiter = ',')

        
        for line in reader:
            #store the data into those arrays
            title.append(line[0])
            xVals.append(float(line[latLocation]))
            yVals.append(float(line[longLocation]))
            
    # close the file automatically.

    # my final array consists of points , not x and y coords, so take those
    # x and y and create new Points.
    finalArray = []
    for i in range(len(xVals)):
        finalArray.append(Point([xVals[i], yVals[i]]))

    # return those points.
    return finalArray

def cleanData(fileToBeCleaned, latLocation, longLocation):
    
    # open the file and create the reader to read the file.
    inp = open(fileToBeCleaned, 'r')
    reader = csv.reader(inp)

    # skip the first line (the header)
    next(reader)

    # make a new data array to store stuff in.
    data = []

    
    for row in reader:
        #if neither latitude or longitude is null
        if (((row[latLocation]) != "") and (row[longLocation] != "")):
            
            #if latitude is in the united states
            if((float(row[latLocation]) > 24.005611) and (float(row[latLocation]) < 48.987386)):
                
                #if longitude is in the United states.
                if((float(row[longLocation]) > -124.62608) and (float(row[longLocation]) < -62.361014)):
                    data.append(row)

    #close the file.
    inp.close()
    
    #create a new file with only the rows I have stored.
    with open('new.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)

    # find the current path, go there, and find the file named new.csv.
    # once I find it, rename it to whatever it was called before.
    
    path = os.path.dirname(os.path.abspath(__file__))
    dirArray = natural_sort(os.listdir(path)) 
    for file in dirArray:
        if file == "new.csv":
            os.remove(fileToBeCleaned)
            os.rename('new.csv', str(fileToBeCleaned))
            return

    
def getDistance(a, b):
    # return the square root of two points A and B using pythagorean formula.
    return math.sqrt(((a.X - b.X)**2) + ((a.Y - b.Y)**2))

"""
    This method is the meat and bones of the entire operation.
    It takes in points as an array of starting points, an integer
    number of clusters, and a cutoff value to stop moving the clusters around
    once the value is reached.
"""
def kMeans(points, numClusters, cutoff):

    # So we have to start with some random clusters, so pick a couple of dots and
    # make those our starting clusters.
    initialCentroids = random.sample(points,numClusters) #make random centroids

    ############### plot initial points ######################

    # store x and y coords of centroids in these two arrays
    xCentroids, yCentroids = [], []
    for i in initialCentroids:
        xCentroids.append(i.X)
        yCentroids.append(i.Y)

    # store all the x and y values of the points in these two arrays
    xVals, yVals = [],[]
    for i in points:
        xVals.append(i.X)
        yVals.append(i.Y)

    #plot using pylab
    pylab.figure(0)
    pylab.title("Initial Points & Centroid")
    
    # NOTE: Plot yVals as x and xVals as y, because latitude is on the y axis technically
    #       and longitude is on the x axis
    
    pylab.plot(yVals, xVals, "bo")
    pylab.plot(yCentroids, xCentroids, "x", c = "r", ms = 13)
    pylab.savefig('Iteration 0.png')
    pylab.close()
    
    ############### end plot initial points ######################

    # this is the array of clusters
    clusterArray = []
    for centroid in initialCentroids:
        clusterArray.append(Cluster([centroid])) # make clusters with just centroid point

    # counter to keep track of what number we are at
    iteration = 0
    
    while True:
        lists = [[] for _ in clusterArray] #list of lists to hold points in cluster
        iteration += 1 # increment iteration number

        for p in points: # for each point

            # get smallest distance
            smallestDistance = getDistance(p,clusterArray[0].centroid) 
            clusterIndex = 0
            for i in range(numClusters - 1):
                distance = getDistance(p, clusterArray[i+1].
                                       centroid)
                # get the distance and see if it is smaller than the smallest distance
                if distance < smallestDistance:
                    smallestDistance = distance
                    clusterIndex = i+1
                    # basically, find what cluster it belongs to
                    
            lists[clusterIndex].append(p) #assign it to that cluster

        # biggestShift in new clusters..
        biggestShift = 0.0

        #loop through all of them
        for i in range(numClusters):
            shift = clusterArray[i].renew(lists[i]) # update cluster with new points
            biggestShift = max(biggestShift, shift) # only store biggest shift

        # plot it!
        plot(clusterArray, iteration)

        #only stop if the biggest shift is smaller than the cutoff value.
        if biggestShift < cutoff:
            print("Done at %s iterations" % iteration)
            print("WAIT UNTIL FINISHED. DO NOT CLOSE")
            break
    return clusterArray, iteration

        
def plot(clusters, iteration):

    #create a new figure based on what iteration it is.
    pylab.figure(iteration)

    #different symbols for the different clusters.
    symbols = ["o", "v", "<", "1", "2", "3", "4", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|"]

    #new title
    pylab.title("Iteration %s" % iteration)
    print("Iteration %s" % iteration)
    
    symbolCounter = -1
    # for each cluster.
    for i in clusters:
        
        # use a different symbol & reset xVals and yVals
        symbolCounter += 1
        xVals, yVals = [],[]

        #for each point, append it to list of x and y
        for ii in i.points:
            xVals.append(ii.Y)
            yVals.append(ii.X)

        #plot all those xvalues and yValues and also the centroid
        pylab.plot(xVals, yVals, symbols[symbolCounter])
        pylab.plot(i.centroid.Y, i.centroid.X, "x",c = "r", ms = 13)

        #print out centroid so I can track its movement
        print(i.centroid.X, i.centroid.Y)
    print("-----------------------------------------------------------")

    # Save the figure and close it.
    pylab.savefig('Iteration %s.png' % iteration)
    pylab.close()

"""
    This takes all png images in the current directory
    and turns them into a gif. The parameter speed specifies
    how fast the images will go by.
"""
def pngToGif(speed):

    # array for the PNG images I find. 
    images = []

    # the working directory
    path = os.path.dirname(os.path.abspath(__file__))
    dirArray = natural_sort(os.listdir(path))

    #for all the files in the current directory, 
    for file in dirArray:
        #if it is a png image
        if file.endswith(".png"):
            
            # read image and add it to the array list
            images.append(imageio.imread(file))

            # delete the file
            os.remove(file)

            # var to hold speed        
            kargs = { 'duration': speed }

            # save image as gif
            imageio.mimsave("animation.gif", images,'GIF', **kargs)

"""
    Just a simple sorting algorithm so I can look through directory.
"""
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

"""
    This is the actual code where I call the methods I wrote and specify the
    values I want to pass as parameters.
"""

#specify cutoff value and speed for gif
cutoff = 0.02
speed = 0.5

# get input on how many clusters I want from my data
numClusters = int(input("How many clusters do you want? "))

# so here are 2 datasets that I have cleaned and prepped, so it should be good to run!

points = importData("Starbucks.csv", 0, 1)
#points = importData("HUD housing.csv", 12, 13)

# actually run the kMeans and store the final cluster array and the number of iterations it
# took to get there. Using the final cluster array, I can perform statistical analysis on this
# and run more tests to gather more information and put it to use. For right now, it just looks
# pretty. :)

finalClusterArray, iterations = kMeans(points, numClusters, cutoff) # run Main code
pngToGif(speed) # make it a GIF
