import pytesseract
import re
import cv2
import requests
from flask import Blueprint, request
from flask_cors import CORS
from enhance.resize import resized_image
from enhance.bright import brightim1
from enhance.crop import crop1
from cards.voters import voteridocr
from cards.passport import passportocr
from cards.licence import driverlic
from cards.cheque import cheque
from utils.IOUtils import config

OCR_app = Blueprint('OCR_app', __name__, url_prefix='/main')
CORS(OCR_app)


@OCR_app.route("/ocr", methods=['POST'])
def process_image():
    content = request.get_json()
    temp_file_path = 'temp/filesent.jpg'

    try:
        text2,final_image = read_image_get_text(content['url1'], temp_file_path)
    except:
        text2 = ""
        pass
    try:
        text1,final_image = read_image_get_text(content['url'], temp_file_path)
    except Exception as e:
        print(e)
        text1 = ""
    imageType = getImageType(text1)

    if imageType == 'DRIVING LICENCE':
        ocrJson = driverlic(text1)
    elif imageType == 'INDIAN PASSPORT':
        ocrJson = passportocr(text1)
    elif imageType == "VOTER'S ID":
        text = text1 + ' ' + text2
        ocrJson = voteridocr(text, text1)
    elif imageType == 'CHEQUE':
        ocrJson = cheque(final_image)
    else:
        ocrJson = 'INVALID DOCUMENT'
    return ocrJson


def getImageType(text):
    lines = ""
    for item in text:
        lines = lines + item
    dlarr = ['LICENCE', 'DRIVING', 'MOTOR', 'UNION', 'DRIVE', 'AUTHORISATION', 'DL No', 'Department']
    passarr = ['PASSPORT', 'REPUBLIC', 'Passpertt','Nationality']
    voterarr = ['ELECTION', 'COMMISSION', 'IDENTITY', 'ELECTOR', 'Electoral', 'Registration', 'Officer','Assembly']
    chequearr = ['IFSC' , 'BANK' , 'Rupees',"Bank"]

    if any(re.findall('|'.join(dlarr), lines)):
        print('Document is Driving Licence')
        document = 'DRIVING LICENCE'
    elif any(re.findall('|'.join(passarr), lines)):
        print("Document is Passport")
        document = "INDIAN PASSPORT"
    elif any(re.findall('|'.join(voterarr), lines)):
        print("Document is Voter's Id")
        document = "VOTER'S ID"
    elif any(re.findall('|'.join(chequearr), lines)):
        print("Document is a Cheque")
        document = "CHEQUE"
    else:
        document = 'INVALID DOCUMENT'
    return document


def read_image_get_text(url1, temp_file_path):
    if len(re.findall("^http[s,S]://", url1)) > 0:
        response = requests.get(url1, stream=True)
        with open(temp_file_path, 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        image = cv2.imread('temp/filesent.jpg')
    else:
        image = cv2.imread(url1)
    print(image.shape)
    resized = resized_image(image)
    imageCrop = crop1(resized)
    imageBright = brightim1(imageCrop)
    text = pytesseract.image_to_string(imageBright, config=config)
    return text,imageBright
