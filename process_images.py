import glob
import cv2
import math

from params import *
#from SimpleITK import Elastix, ReadImage, WriteImage

#if __name__ == 'main':

newsize = 299
rootdir = './Images'
for dir in glob.glob('./Images/*/*/'):
	for subdir in glob.glob(dir + '/*'):
		for file in glob.glob(subdir + '/*.jpg'):
			print(file)
			img = cv2.imread(file)
			height, width, channels = img.shape
			x = math.floor((width - newsize)/2)                 #should be 106
			y = math.floor((height - newsize)/2)                #should be 106
			img_crop = img[y:y+newsize, x:x+newsize]     #copy is optional, crop should go from 106 to 405
			cv2.imwrite(file, img_crop)

	'''
	TODO:      
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
	    
	import SimpleITK as sitk
	elastixImageFilter = sitk.ElastixImageFilter()
	elastixImageFilter.SetFixedImage(sitk.ReadImage("fixedImage.nii")
	elastixImageFilter.SetMovingImage(sitk.ReadImage("movingImage.nii")
	elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("affine"))
	elastixImageFilter.Execute()
	sitk.WriteImage(elastixImageFilter.GetResultImage())
	'''
