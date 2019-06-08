import glob
import cv2
import math
import os
import pyelastix
import imageio
import threading
#import SimpleITK as sitk

from params import *
#from SimpleITK import Elastix, ReadImage, WriteImage

#if __name__ == 'main':


#
## IF YOU'RE READING THIS THE PROCESSING WORKED
#

'''
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
template1 = imageio.imread('./Images/Templates/1.jpg')
template2 = imageio.imread('./Images/Templates/2.jpg')
template3 = imageio.imread('./Images/Templates/3.jpg')

templates = [template1[:,:,1].astype('float32'), template2[:,:,1].astype('float32'), template3[:,:,1].astype('float32')]

params = pyelastix.get_default_params(type='AFFINE')
params.NumberOfResolutions = 2


def register(arg1, arg2):
	files = arg1
	template = arg2
	for file in files:
		print(file)
		cur_image = imageio.imread(file)
		cur_image = cur_image[:,:,1].astype('float32')
		output_image = None
		output_image, field = pyelastix.register(cur_image, template, params, exact_params=False, verbose=0)
		imageio.imwrite(file,output_image)


for dir in glob.glob('./Images/*/*/'):
	for subdir in glob.glob(dir + '/*'):
		list = os.listdir(subdir)
		number_files = len(list)
		third = number_files//3
		counter = 0
		image_sets = [[], [], []]
		for file in glob.glob(subdir + '/*.jpg'):
			if counter < third:
				image_sets[0].append(file)
			elif counter < 2*third:
				image_sets[1].append(file)
			else:
				image_sets[2].append(file)
			counter += 1
		threads = []
		for i in range(3):
			x = threading.Thread(target=register, args=(image_sets[i], templates[i]))
			threads.append(x)
			x.start()
		for index, thread in enumerate(threads):
			thread.join()
		
	
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
