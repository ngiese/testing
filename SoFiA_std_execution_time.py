#!/usr/bin/env python

## config
# sizes of cubes to calculate the std from
cubeSizes = [50,100,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000]
# standard deviation of Gaussian
sigma = 3

## imports
import os
from numpy.random import normal
from numpy import std
from math import sqrt
from time import time
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc

## functions
def mirror_std(data):
    data[::2] *= -1
    s = std(data)
    return s

def std_zeroMean(data):
    s = sqrt(((data**2).sum())/data.shape[0])
    return s
    
## directory where script is located 
## the output plot will be stored there
scriptPath = ('/').join(os.path.realpath(__file__).split('/')[0:-1])


## create cubes and store the execution times
duration1 = []
duration2 = []
cubeNum = len(cubeSizes)
for i in range(cubeNum):
    try:
        # create cubes with random normal variables   
        N = int(cubeSizes[i])
        cube = normal(scale=sigma,size=(N,N,N))

        # select only the negative values
        negativeValues = cube[cube<0]
        
        #method1
        start = time()
        std1 = std_zeroMean(negativeValues)
        end = time()
        duration1.append(end-start)    
        
        # method 2
        start = time()
        std2 = mirror_std(negativeValues)
        end = time()
        duration2.append(end-start)
    except:
        print 'memory not sufficient for cube of size (%d,%d,%d)'%(N,N,N)

del cube, negativeValues

rc('figure',figsize=(8,6))
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'],'size' : 17})
rc('text', usetex=True)

## plot the results
#  sort the duration arrays by time (in case the user provided cube sizes in random order)
times = zip(duration1,duration2,cubeSizes)
times.sort()
duration1, duration2, cubeSizes = zip(*times)
# scatter plot of the duration data
plot = plt.scatter(duration1,duration2,c=cubeSizes,cmap='gist_rainbow')
plt.colorbar(plot,label='$(\mathrm{cube\ size})^{1/3}\ [\mathrm{px}]$')
# one-to-one line
maxRange = max(duration1+duration2)
minRange = min(duration1+duration2)
plt.plot([minRange,maxRange],[minRange,maxRange])
plt.xlabel('execution time zero mean [s]')
plt.ylabel('execution time mirror values [s]')
# save figure
plt.savefig(os.path.join(scriptPath,'comparison.png'))




