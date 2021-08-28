import pytesseract
import numpy as np
from PIL import Image, ImageEnhance


def brightim1(img):
	lenth_list = []
	image_list = []
	dict1 = {}
	img = Image.fromarray(img)

	text = pytesseract.image_to_string(img, lang='eng')
	length = len(text)
	lenth_list.append(length)
	image_list.append(img)
	print("list1: " , lenth_list)
	enhancer1 = ImageEnhance.Brightness(img)
	im1 = enhancer1.enhance(2.5)
	text1 = pytesseract.image_to_string(im1, lang='eng')
	length1 = len(text1)
	lenth_list.append(length1)
	image_list.append(im1)

	enhancer2 = ImageEnhance.Brightness(img)
	im2 = enhancer2.enhance(2.8)
	text2 = pytesseract.image_to_string(im2, lang='eng')
	length2 = len(text2)
	lenth_list.append(length2)
	image_list.append(im2)

	enhancer3 = ImageEnhance.Brightness(img)
	im3 = enhancer3.enhance(3.0)
	text3 = pytesseract.image_to_string(im3, lang='eng')
	length3 = len(text3)
	lenth_list.append(length3)
	image_list.append(im3)

	# enhancer4 = ImageEnhance.Brightness(img)
	# im4 = enhancer4.enhance(3.5)
	# text4 = pytesseract.image_to_string(im4, lang='eng')
	# length4 = len(text4)
	# lenth_list.append(length4)
	# image_list.append(im4)

	enhancer5 = ImageEnhance.Brightness(img)
	im5 = enhancer5.enhance(2.0)
	text5 = pytesseract.image_to_string(im5, lang='eng')
	length5 = len(text5)
	lenth_list.append(length5)
	image_list.append(im5)

	enhancer6 = ImageEnhance.Brightness(img)
	im6 = enhancer6.enhance(2.6)
	text6 = pytesseract.image_to_string(im6, lang='eng')
	length6 = len(text6)
	lenth_list.append(length6)
	image_list.append(im6)



	print("image:" , image_list[np.argmax(np.array(lenth_list))])
	print("length list:" , lenth_list)
	print("image_list:",image_list)

	return  image_list[np.argmax(np.array(lenth_list))]