from tabnanny import check
import numpy as np
import pytesseract
import cv2
import string
import os
from os import listdir
from os.path import isfile, join

# enhance image for better text extraction. Takes an image and returns ehanced image


def enhanceText(img):
	
	img = cv2.resize(img, None, fx=2, fy=2,
					interpolation=cv2.INTER_CUBIC)  # bigger image size

	img = cv2.blur(img, (5, 5))  # blurring
	img = cv2.bilateralFilter(img, 9, 75, 75)  # filter for text extract

	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # gray image
	return img

# preprocess the extracted text for word isolation and remove unneccessary punctions and symbol


def preprocessText(text):
	text = text.lstrip().rstrip()
	text = text.translate(str.maketrans(
		'', '', string.punctuation))  # remove punctuation
	return text

# from an image it detect rectangle shape with an area threshold parameter, saves the images extracting text from same image


def detectRect(image_path, absolute_dir, area_treshold=200000):

	# load the image
	image = cv2.imread(image_path)
	# grayscale
	result = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# adaptive threshold
	thresh = cv2.adaptiveThreshold(
		gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 9)

	# Fill rectangular contours
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	for c in cnts:
		cv2.drawContours(thresh, [c], -1, (255, 255, 255), -1)

	# Morph open
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

	# Draw rectangles, the 'area_treshold' value was determined empirically
	cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	ROI_number = 0
	for c in cnts:
		if cv2.contourArea(c) > area_treshold:
			x, y, w, h = cv2.boundingRect(c)
			# cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
			# gives our desired image
			crop = image[y:y+h, x:x+w]

			Image_ht, Image_wd, Image_thickness = crop.shape
			# cropped the text portion of the image
			Sample_Text = crop[690:Image_ht-5, 390:Image_wd-5]

			# enhance the text portion image
			Sample_img = enhanceText(Sample_Text)

			custom_config = r'--oem 3 --psm 6'
			# extract text from image
			some_text = pytesseract.image_to_string(
				Sample_img, lang='eng', config=custom_config,timeout=0.5)
			# preprocess the image
			some_text = preprocessText(some_text)
			print(some_text)
			os.chdir(absolute_dir)

			if some_text == "" :
				cv2.imwrite(str(ROI_number)+'.png', crop)
			else:
				cv2.imwrite(some_text+'.png', crop)
			ROI_number += 1

if __name__ == "__main__":
	# main image path
	image_dir = r'F:\sems12\cse499\chosen_images'.format('')
	# tesseract cmd path windows
	tess = r'C:\Program Files\Tesseract-OCR\tesseract.exe'.format('')
	pytesseract.pytesseract.tesseract_cmd = tess
	# where to save your cropped images
	absolute_dir = r'F:\sems12\cse499\testing'.format(
		'')
	#create if directory not exist
	if not os.path.exists(absolute_dir):
		os.mkdir(absolute_dir)
		print("Directory " , absolute_dir ,  " Created ")

	onlyfiles = os.listdir(image_dir)
	onlyDirs = [os.path.join(image_dir,f) for f in onlyfiles]
	
	print("Total Images:",len(onlyfiles))
	counter = 0
	for img_dir in onlyDirs:
		print(counter)
		counter += 1
		detectRect(img_dir,absolute_dir)
