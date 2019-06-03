import os
import cv2
import math

from params import *
from SimpleITK import Elastix, ReadImage, WriteImage

if __name__ == 'main':
    '''
    TODO:
    1.  Recursively loop through ./Images, taking each 512x512 image and cropping it
        to the middle 299x299 square
        
        newsize = 299
        rootdir = './Images'
        for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    if file.endswith(".jpg"):
                        img = cv2.imread(file)
                        height, width, channels = img.shape
                        x = math.floor((width - newsize)/2)                 // should be 106
                        y = math.floor((height - newsize)/2)                // should be 106
                        img_crop = img[y:y+newsize, x:x+newsize].copy()     // copy is optional, crop should go from 106 to 405
                        //Place image wherever
            
    2.  Figure out a way to register each of the non-template images (i.e. not the images 
        in ./Images/Templates) such that they are all reasonably aligned. 
        This is probably the tool you want to use: https://simpleelastix.readthedocs.io/
        The not-yet-cropped images in ./Images/Templates may serve as good reference images;
        you could register the first 1/3 of the images in each subdirectory to 1.jpg, the next
        1/3 to 2.jpg, and the remaining ones to 3.jpg. Just check to make sure the resulting
        images actually appear to be aligned, and that image quality is not significantly
        compromised.
        
        It's fine to change file names, just make sure the alphanumeric ordering of the original 
        file names is preserved by this script, as well as the directory names.
    '''
