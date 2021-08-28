import re
from flask import jsonify
def driverlic(text):
	print(text)
	lines = ""
	for item in text:
		lines = lines + item
	lines = lines.replace("Transport", '')
	lines = lines.replace("TRANSPORT", '')

	name = get_name(lines)
	Dob = get_dob(lines)
	dl = get_dl(lines)
	ID = get_id(lines)
	VD = get_vd(lines)
	uid = get_ano(lines)
	rel = get_relation(lines)
	blood = get_bg(lines)
	add2 = get_address(lines)
	p3 = get_pin(lines)
	cov = get_cov(lines)
	list4 = get_covdoi(lines)

	data = {}
	data['name'] = name
	data['DateofBirth'] = Dob
	data['DriversLicenceNumber'] = dl
	data['IssuingDate'] = ID
	data['ValidDate'] = VD
	data['AadharNumber'] = uid
	data['S/W/D'] = rel
	data['BloodGroup'] = blood
	data['Address'] = add2
	data['Pin'] = p3
	data['Typeofvehicleauthorizedtodrive'] = cov
	data['Vehicleissuedateavailable'] = list4
	return jsonify(data)

def get_name(lines):
	try:
		
		nameObj = re.search('(?<=Name)(.*$)|(?<=Name:)(.*$)|(?<=Vame)(.*$)', lines, re.M|re.I)
		name = nameObj.group()
		name = re.sub('[^A-Z ]+',"", name)
		name = re.sub('^\s+|\s+\Z', "", name)
	except:
		print('Name not found')
		name = ""
	return name

def get_dob(lines):
	try:
		
		DobObj = re.search('(?<=DT.OF BIRTH :)(.*$)|(?<=DOB)(.*$)|(?<=HOB)(.*$)', lines, re.M|re.I)
		Dob = DobObj.group()
		Dob = re.sub('^\s+|\s+\Z', "", Dob)
		Dob= re.sub('[A-Z|a-z]+', "", Dob)
		Dob= re.sub('[( )|()]', "", Dob)
		Dob= re.sub('[#]', "", Dob)
		print("date of birth", Dob)
	except:

		print("Date of birth not found")
		Dob = ""

	return Dob



def get_dl(lines):
	try:
		dlObj = re.search('[A-Z]{2}[0-9]{2}\s[0-9]{11}|[A-Z]{3}[0-9]{1}\s[0-9]{11}|[A-Z]{2}[-][0-9]{13}', lines, re.M | re.I)
		dl = dlObj.group()
	except:
		try:

			dlObj = re.search('(?<=DL NO)(.*$)|(?<=DLNUMBER)(.*$)|(?<=DL)(.*$)|(?<=Licence No.)(.*$)', lines, re.M | re.I)
			dl = dlObj.group()
			dl = re.sub('I', '1', dl)
			dl = re.sub('i', '1', dl)
			dl = re.sub('[^0-9]+', "", dl)

		except:
			dl = ""
	return dl

def get_id(lines):
	try:
		
		IDObj = re.search('(?<=DO)(.*$)|(?<=Date of issue)(.*$)|(?<=DT. OF ISSUE)(.*$)|(?<=DOI)(.*$)|(?<=DO!)(.*$)|(?<=DO! :)(.*$)|(?<=id)(.*$)|(?<=ID)(.*$)|(?<=Issue Date)(.*$)' , lines, re.M|re.I)
		ID = IDObj.group()
		ID = re.sub('^\s+|\s+\Z', "", ID)
		ID= re.sub('[( )|()]', "", ID)
		ID= re.sub('[#]', "", ID)
		ID= re.sub('[A-Z|a-z]+', "", ID)

	except:
		try:
			IDObj = re.findall('\d{2}[/]\d{2}[/]\d{4}', lines, re.M | re.I)
			ID = IDObj.group()
		except:
			ID = ""
	return ID



def get_vd(lines):
	try:
		
		VDObj = re.search('(?<=Validity)(.*$)|(?<=Valid Till)(.*$)|(?<=Vandi”)(.*$)|(?<=Yah)(.*$)', lines, re.M|re.I)
		VD = VDObj.group()
		VD = re.sub('^\s+|\s+\Z', "", VD)
		VD= re.sub('[A-Z|a-z]+', "", VD)
		VD= re.sub('[( )|()]', "", VD)
		VD= re.sub('[#]', "", VD)
	except:
		VD=""
	return VD


def get_ano(lines):
	try:
		
		uidObj = re.search('[0-9]{4}\s[0-9]{4}\s[0-9]{4}', lines, re.M|re.I)
		uid = uidObj.group()
		uid = re.sub('^\s+|\s+\Z', "", uid)

	except:
		try:
			uidObj = re.search('[0-9]{4}\s[0-9]{4}\s[0-9]{4}', "", re.M | re.I)
			uid = uidObj.group()
			uid = re.sub('^\s+|\s+\Z', "", uid)

		except:
			uid = ""
	return uid



def get_relation(lines):
	try:
		
		relObj = re.search('(?<=S/DAW of)(.*$)|(?<=S/DM of:)(.*$)|(?<=3/D/W of)(.*$)|(?<=S/W/D)(.*$)|(?<=S/W/D of)(.*$)|(?<=S/D/W of)(.*$)|(?<=S/DMW of)(.*$)|(?<=siW/D)(.*$)|(?<=Daughter of)(.*$)|(?<=S/DW of)(.*$)|(?<=Daughier of :)(.*$)' , lines, re.M|re.I)
		rel = relObj.group()
		rel = re.sub('[^A-Za-z ]+',"", rel)
		rel = re.sub('^\s+|\s+\Z', "", rel)
	except:
		rel=""
	return rel

def get_bg(lines):
	try:
		
		bloodObj = re.search('(?<=BG:)(.*$)|(?<=Blood group)(.*$)|(?<=Blood)(.*$)', lines, re.M|re.I)
		blood = bloodObj.group()
	except:
		blood = ""
	return blood



def get_address(lines):
	try:
		#Address
		addObj = re.compile('(?<=AAdc_SR)(.*$)|(?<=Address)(.*$)|(?<=Add)(.*$)', re.IGNORECASE | re.DOTALL).search(lines)
		add = addObj.group()
		add1 = add.split('\n')
		add2 = add1[0],add1[1],add1[2]

	except:
		add2 = ""
	return add2


def get_pin(lines):
	try:
		
		pinObj = re.compile('(?<=Pin)(.*$)', re.IGNORECASE | re.DOTALL).search(lines)
		pin = pinObj.group()
		pin = re.sub('[^0-9]+', "", pin)
		pin = re.sub('i', '1', pin)
		pin = re.sub('I', '1', pin)
		p3 = pin[:6]

	except:
		p3 = ""
	return p3


def get_cov(lines):
	try:

		covl = 'MC 50CC|MC EX50CC|CYCL.WOG|MCWG|M/CYCL.WG|MCWOG|LMV|LMV-NT|LMV-TR|LDRXCV|HMV|HPMV|HTV|TRAILERE|INVCRG|mcy|omy|Mey|wewos|trans|TRANS'
		cov = re.findall(covl,lines,re.IGNORECASE)

	except:
		cov= ""
	return cov

def get_covdoi(lines):
	try:
		cov2 = '(?<=MC 50CC)(.*$)|(?<=MC EX50CC)(.*$)|(?<=CYCL.WOG)(.*$)|(?<=MCWG)(.*$)|(?<=M/CYCL.WG)(.*$)|(?<=MCWOG)(.*$)|(?<=LMV)(.*$)|(?<=LMV-NT)(.*$)|(?<=LMV-TR)(.*$)|(?<=LDRXCV)(.*$)|(?<=HMV)(.*$)|(?<=HPMV)(.*$)|(?<=HTV)(.*$)|(?<=TRAILERE)(.*$)|(?<=INVCRG)(.*$)|(?<=mcy)(.*$)|(?<=McWe)(.*$)|(?<=omy)(.*$)|(?<=Mey)(.*$)|(?<=wewos)(.*$)|(?<=TRANS)(.*$)'
		cov1 = re.findall(cov2, lines, re.M )
		list4 = []
		for i in range(len(cov1)):
			p = cov1[i]
			for j in p:
				if (j!=''):

					j = re.sub('[^0-9|/|-]+',"", j)
					list4.append(j)
					i=i+1
	except:
		list4 = []
	return list4








	


	


