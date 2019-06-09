import glob
import cv2
import math
import os
import pyelastix
import imageio
import threading

from params import *

#Crops all images to desired 299x299 size.
newsize = 299
for dir in glob.glob('./Images/*/*/'):
	for subdir in glob.glob(dir + '/*'):
		for file in glob.glob(subdir + '/*.jpg'):
			print(file)
			img = cv2.imread(file)
			height, width, channels = img.shape
			x = math.floor((width - newsize)/2)          
			y = math.floor((height - newsize)/2)                
			img_crop = img[y:y+newsize, x:x+newsize]
			cv2.imwrite(file, img_crop)

#Gets template images for registration.
template1 = imageio.imread('./Images/Templates/1.jpg')
template2 = imageio.imread('./Images/Templates/2.jpg')
template3 = imageio.imread('./Images/Templates/3.jpg')

templates = [template1[:,:,1].astype('float32'), template2[:,:,1].astype('float32'), template3[:,:,1].astype('float32')]

params = pyelastix.get_default_params(type='AFFINE')
#Sets desired resolution, higher resolution the better.
params.NumberOfResolutions = 2

#Function to register group of images to one tempalte
def register(files, template):
	for file in files:
		print(file)
		cur_image = imageio.imread(file)
		cur_image = cur_image[:,:,1].astype('float32')
		output_image = None
		output_image, field = pyelastix.register(cur_image, template, params, exact_params=False, verbose=0)
		imageio.imwrite(file,output_image)

#Registers all images to the desired template.
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