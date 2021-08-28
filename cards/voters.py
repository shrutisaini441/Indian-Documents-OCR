import re
from flask import jsonify


def voteridocr(text="", text1=""):
    print(text)
    lines = ""

    for item in text:
        lines = lines + item
    txt = text1.replace('\n', " ")

    data = {}
    data['name'] = get_voter_name(txt, text1)
    data['Voterid'] = get_voter_id(lines)
    data['Fathersname'] = get_fathers_name(txt, text1)
    data['gender'] = get_gender(lines)
    data['dob'] = get_dob(lines)
    #data['add'] = get_address(lines)

    return jsonify(data)


def get_voter_id(lines):
    try:
        voter_obj = re.search("[A-Z]{3}[/][0-9]{7}|[A-Z]{3}[0-9]{7}", lines + lines.replace("O","0"), re.M | re.I)
        voter = voter_obj.group()
    except:
        try:
            voter_obj = re.search("[A-Z]{2}[0-9]{7}", lines, re.M | re.I)
            voter = voter_obj.group()
        except:
            voter = " "
    return voter


def get_voter_name(txt, text1):
    try:
        nameObj = re.search(
            '(?<=“Name :. )(.*$)|(?<=ELECTOR’S NAME)(.*$)|(?<=ectrename)(.*$)|(?<=Electors Name)(.*$)|(?<=Name)(.*$)',
            text1, re.M | re.I)
        name1 = nameObj.group()
        name1 = re.sub('[:]+', "", name1)
        if name1 == '':
            names = txt.split('+')
            name1 = names[1]
        else:
            pass
    except:
        try:
            names = txt.split('+')
            name1 = names[1]
        except:
            try:
                names = txt.split(':')
                name1 = names[1]
            except:
                name1 = ""
    return name1


def get_fathers_name(txt, text1):
    try:
        fatherObj = re.search(
            "(?<=FATHER'S NAME:)(.*$)|(?<=Father's Name)(.*$)|(?<=Father:)(.*$)|(?<=Father's Nama:)(.*$)", text1,
            re.M | re.I)
        father1 = fatherObj.group()
        father1 = re.sub('[:]+', "", father1)
        father12 = father1
        if father1 == '':
            fathers = txt.split('+')
            father1 = fathers[2]
            if father1 == '':
                fathers = txt.split(':')
                father1 = fathers[2]
        else:
            pass

    except:
        try:
            fathers = txt.split('+')
            father1 = fathers[2]
        except:
            try:
                fatherObj = re.search("(?<=FATHER)(.*$)|(?<=father)(.*$)", text1, re.M | re.I)
                father1 = fatherObj.group()
            except:
                try:
                    fathers = txt.split(':')
                    father1 = fathers[2]
                except:
                    father1 = ""
    return father1


def get_gender(lines):
    try:
        genderObj = re.search('(?<=Sex )(.*$)', lines, re.M | re.I)
        gender = genderObj.group()
        gens = gender.split("/")
        gen = gens[1]
    except:
        try:
            genderObj1 = re.search('(?<=Female )(.*$)|(?<=Female)(.*$)', lines, re.M | re.I)
            if genderObj1 != None:
                gen = "Female"
            else:
                gen = "Male"
        except:
            gen = ""
    return gen


def get_dob(lines):
    try:
        dateObj = re.search('\d{2}[/]\d{2}[/]\d{4}', lines, re.M | re.I)
        date = dateObj.group()
    except:
        try:
            dateObj = re.search('\d{2}[/]\d{2}[/]\d{4}[/]\d{2}|\d{1}[/]\d{1}[/]\d{4}[/]\d{2}', lines, re.M | re.I)
            date = dateObj.group()
        except:
            try:
                dateObj = re.search('\d{2}[.]\d{2}[.]\d{4}|\d{1}[.]\d{1}[.]\d{4}', lines, re.M | re.I)
                date = dateObj.group()
            except:
                try:  # dob
                    dateObj = re.search('\d{2}[-]\d{2}[-]\d{4}|\d{1}[-]\d{1}[-]\d{4}', lines,
                                        re.M | re.I)
                    date = dateObj.group()
                except:
                    date = " "
    return date
