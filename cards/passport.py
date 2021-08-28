import re
from flask import jsonify



def passportocr(text):
    #print(text)
    lines = ""
    for item in text:
        lines = lines + item
    lines = lines.replace("REPUBLIC OF INDIA", '')
    lines = lines.replace("OF INDIA", '')
    lines = lines.replace("P ND '", '')
    lines = lines.replace("Woe", '')

    surnameObj1 = lines.split('\n')
    caps = [c for c in surnameObj1 if c.isupper()]
    surname1 = caps[0]
    surname1 = re.sub('[0-9]', "", surname1)
    line1 = lines
    if (len(surname1) == 2) | (len(surname1) == 1):
        line1 = lines.replace(surname1, '')

    gen = get_gender(lines)
    dob = get_dob(lines)
    doe = get_doe(lines)
    doi = get_doi(lines)
    nat = get_nat(lines)
    name = get_name(line1,lines)
    surname = get_surname(line1,lines)
    passport_no = get_passport_no(lines)
    pob = get_place_of_birth(line1)
    poi = get_place_of_issue(line1)

    data = {}
    data['name'] = name
    data['gender'] = gen
    data["date of birth:"] = dob
    data["date of issue:"] = doi
    data["date of expiry"] = doe
    data["nationality"] = nat
    data['surname:'] = surname
    data['Passport Number'] = passport_no
    data['Place of birth'] = pob
    data['place of issue'] = poi
    return jsonify(data)


def get_gender(lines):
    try:
        genObj = re.search('(?<=INDIAN)(.*$)', lines, re.M | re.I)
        gen = genObj.group()
        gen = re.sub('[^A-Z ]+', "", gen)
        gen = re.sub('^\s+|\s+\Z', "", gen)
        print("gender:", gen)
    except:
        print('Gender not found')
        gen = ""
    return gen


def get_dob(lines):
    try:
        dateObj = re.findall('\d{2}[/]\d{2}[/]\d{4}', lines, re.M | re.I)
        dob = dateObj[0]
    except:
        dob = ""
        print("not found")
    return dob


def get_doe(lines):
    try:
        dateObj = re.findall('\d{2}[/]\d{2}[/]\d{4}', lines, re.M | re.I)
        doe = dateObj[2]
        print("date of expiry", doe)
    except:
        print("not found")
        doe = ""
    return doe


def get_doi(lines):
    try:
        dateObj = re.findall('\d{2}[/]\d{2}[/]\d{4}', lines, re.M | re.I)
        doi = dateObj[1]
        print("date of issue:", doi)
    except:
        print("not found")
        doi = ""
    return doi


def get_nat(lines):
    try:
        natObj = re.search('INDIAN|indian', lines, re.M | re.I)
        nat = natObj.group()
        print("Country Code:" , nat)
    except:
        try:
            stext = lines.split('<')
            print(stext)
            print("type:", stext[0][-1])
            print(stext[1])
            if (stext[1][:3] == 'IND'):
                nat = "IND"
                print("Country Code: IND")
            else:
                nat = ""
                print("Country Code not available")
        except:
            print("Not available")
            nat = " "
    return nat


def get_surname(line1,lines):
    try:
            surnameObj = line1.split('\n')
            # print("surname",surname)
            caps = [c for c in surnameObj if c.isupper()]
            # print("caps" , caps)
            surname = caps[0]
            print("surname", surname)
            print("1")

    except:
        try:
            surnameObj = line1.split('\n')
            # print("surname",surname)
            caps = [c for c in surnameObj if c.isupper()]
            #print("caps" , caps)
            surname = caps[0]
            print("surname", surname)
            #print("3")
        except:
            try:
                stext = lines.split('<')
                surname = stext[1][3:]
                #print("4")
                print("surname:", stext[1][3:])
            except:
                surname = " "
                print("No surname")

    return surname


def get_name(line1,lines):
    try:
        nameObj = line1.split('\n')
        #print("surname",surname)
        caps = [c for c in nameObj if c.isupper()]
        #print("caps" , caps)
        name = caps[1]
        name = re.sub('[_]', "", name)
        print("name: " , name)
        print("2")
    except:
        try:
            stext = lines.split('<')
            name = stext[3] + stext[4] + stext[5]
            print("1")
            print("name:", stext[3], stext[4], stext[5])
        except:
            print("name not available")
            name = ""
            pass
    return name


def get_passport_no(lines):
    try:
        pnObj = re.search('[A-Z]{1}[0-9]{7}',lines,re.M | re.I)
        s1 = pnObj.group()
        print("passport number:", s1)
    except:
        try:
            stext = lines.split('<')
            s1 = stext[10]
            s1 = re.sub('[c|e]+', "", s1)
            print("passport number:", s1)

        except:
            print("no passport number")
            s1 = ""
    return s1


def get_place_of_birth(line1):
    pob = " "
    try:
        pobObj = line1.split('\n')
        # print("surname",surname)
        caps = [c for c in pobObj if c.isupper()]
        # print("caps" , caps)
        pob = caps[3]
        pob = re.sub('[“]', "", pob)
        print("pob: ", pob)
    except:
        try:
            stext1 = line1.split('\n')
            i = 0
            for i in range(len(stext1)):
                if ("Place of Birth" in stext1[i]):

                    pob = stext1[i + 2]
                    pob = re.sub('^\s+|\s+\Z', "", pob)
                    pob = re.sub('[^A-Z- ]+', "", pob)
                    print("Place of Birth:", pob)
                else:
                    pob = ""
        except:
            print("Place of Birth not found")
            pob = " "
    return pob


def get_place_of_issue(line1):
    try:
        poiObj = line1.split('\n')
        caps = [c for c in poiObj if c.isupper()]
        print("caps" , caps)
        poi = caps[4]
        poi = re.sub('[0-9]', "", poi)
    except:
        try:
            stext1 = line1.split('\n')
            for i in range(len(stext1)):
                if ("Place of issue" in stext1[i]):
                    poi = stext1[i + 2]
                    poi = re.sub('^\s+|\s+\Z', "", poi)
                    poi = re.sub('[^A-Z- ]+', "", poi)

                else:
                    poi = ""
        except:
            print("not available place of issue")
            poi = ""
    return poi
