from flask import jsonify,Flask
import pytesseract
from PIL import Image
import json
import re
import requests

app = Flask(__name__)

@app.route("/chequeOCR", methods = ['POST'])

def cheque(image):
    basewidth = 2000
    img = image
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.show()
    text = pytesseract.image_to_string(img)
    lines = ""
    print(text)
    for item in text:
        lines = lines + item
    res = lines

    list1 = res.split('\n')
    try:
        list1.remove("Please sign above")
    except:
        pass
    IFSC = get_IFSCode(lines)
    acNo1 = get_acNo(lines)
    Name = get_name(list1)
    data = {}
    data['IFSCode'] = IFSC
    data['AccountNumber'] = acNo1
    data['Name'] = Name

    headers = {'DY-X-Authorization': '860328651138502082d9b367353d5bcef7c32c3f'}
    url = 'https://ifsc.datayuge.com/api/v1/'
    r = requests.get(url + IFSC, headers=headers, verify=False)
    ifscApiResponse = json.loads(r.text)
    print(json.dumps(ifscApiResponse, indent=4))
    data['ifscApiResponse'] = ifscApiResponse
    return jsonify(data)

def get_IFSCode(lines):
    try:
        IFSCode = re.search('(?<=IFSC Code)(.*$)|(?<=IFS CODE)(.*$)|(?<=Code)(.*$)|(?<=IFS Code)(.*$)|(?<=SC =)(.*$)|(?<=FSC)(.*$)', lines, re.I|re.M)
        IFSC = IFSCode.group()
        IFSC = IFSC.replace(')', '1')
        IFSC = IFSC.replace('o', 'O')
        IFSC = IFSC.replace('s', '5')
        IFSC = re.sub(':',"", IFSC)
        IFSC = re.sub('^[a-zA-Z0-9_]',"", IFSC)
        slist = IFSC.split()
        print("list:",slist)
        for i in range(len(slist)):
            if slist[i].isalnum() == True:
                IFSC = slist[i]
            else:
                continue

        for i in range(4,len(IFSC)-1):
            if IFSC[i] == 'O':
                IFSC = IFSC[:i] + '0' + IFSC[i+1:]
            elif IFSC[i] == 'S':
                IFSC = IFSC[:i] + '5' + IFSC[i + 1:]
            else:
                continue
        for j in range(0,3):
            if IFSC[j] == '5':
                IFSC = IFSC[:i] + 'S' + IFSC[i + 1:]
        print("IFSCode:",IFSC)
    except:
        try:
            IFSCode = re.search('\w{11}', lines, re.I | re.M)
            IFSC = IFSCode.group()
            IFSC = IFSC.replace('o', 'O')
            IFSC = re.match('.*[a-zA-Z0-9].*', IFSC)
            IFSC = IFSC.group()

            for i in range(4, 11):
                if IFSC[i] == 'O':
                    IFSC = IFSC[:i] + '0' + IFSC[i + 1:]
                if IFSC[i] == 'S':
                    IFSC = IFSC[:i] + '5' + IFSC[i + 1:]
            for j in range(0, 3):
                if IFSC[j] == '5':
                    IFSC = IFSC[:i] + 'S' + IFSC[i + 1:]
            print("IFSC" , IFSC)
        except:
            IFSC = " "
    return IFSC


def get_acNo(lines):
    try:
        acNo = re.search('(?<=Ache.)(.*$)|(?<=Ale)(.*$)|(?<=No)(.*$)|(?<=AccNo)(.*$)', lines, re.I|re.M)
        acNo1 = acNo.group()
        acNo1 = re.sub('[^0-9]+', "", acNo1)
        acNo1 = re.sub('[^0-9]+',"", acNo1)
    except:
        try:
            acNo = re.search('[0-9]{16}|[0-9]{14}|[0-9]{12}|[0-9]{11}|[0-9]{10}|[0-9]{9}', lines, re.M|re.I)
            acNo1 = acNo.group()
        except:
            try:
                acNo = re.search('\d{16}|\d{14}|\d{12}|\d{11}|\d{10}', lines, re.M | re.I)
                acNo1 = acNo.group()
            except:
                acNo1 = " "

    return acNo1


def get_name(list1):
    Name = list1[-1]
    print("name of the account holder: ", Name)
    return Name



if __name__ == '__main__':
    app.run(debug=True)
