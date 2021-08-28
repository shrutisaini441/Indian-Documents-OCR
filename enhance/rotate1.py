import pytesseract
import re
import imutils

def rotate1(image123):
    im = image123
    text = pytesseract.image_to_string(im, lang='eng')
    nameObj = re.search('(?<=licence)(.*$)|(?<=transport)(.*$)|(?<=Name)(.*$)|(?<=DRIVE)(.*$)|(?<=IDENTITY)(.*$)|(?<=ELECTION)(.*$)|(?<=address)(.*$)|(?<=Bank)(.*$)|(?<=Rupees)(.*$)', text, re.M | re.I)
    width, height = im.size
    if (height > width):
        if (nameObj == None):  # if image in portrait form
            rotimage = imutils.rotate(im,270)
            again = pytesseract.image_to_string(rotimage, lang='eng')
            againObj = re.search('(?<=licence)(.*$)|(?<=transport)(.*$)|(?<=Name)(.*$)|(?<=DRIVE)(.*$)|(?<=IDENTITY)(.*$)|(?<=ELECTION)(.*$)(?<=address)(.*$)|(?<=Bank)(.*$)|(?<=Rupees)(.*$)', again, re.M | re.I)
            if (againObj != None):
                return rotimage
            else:
                return im

    elif (width >= height):
        if (nameObj == None):
            rotimage = imutils.rotate(im,180)
            again = pytesseract.image_to_string(rotimage, lang='eng')
            againObj = re.search(
                '(?<=licence)(.*$)|(?<=transport)(.*$)|(?<=Name)(.*$)|(?<=DRIVE)(.*$)|(?<=IDENTITY)(.*$)|(?<=ELECTION)(.*$)(?<=address)(.*$)(?<=Bank)(.*$)|(?<=Rupees)(.*$)',
                again, re.M | re.I)
            if (againObj != None):
                return rotimage
            else:
                return im
        else:
            return im
    return im
