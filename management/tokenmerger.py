from pathlib import Path
from datetime import date
from xml.etree import ElementTree as ET

# Blacklist for .json files
FILEIGNORE = ['Ascention.xml']

# Finding out the TODAY date in DD-MM-YYYY format
today = date.today().strftime('%d-%m-%Y') # Пример: '19-05-2025'

# Getting set files directory
setFilesDir = Path(__file__).parent.parent / 'data'
setFilesDir.mkdir(exist_ok=True)

# Getting and updating patch counter
try:
	with open('patchcount', 'r', encoding='utf-8') as file:
		patchcount = int(file.readline()) + 1
except FileNotFoundError:
	patchcount = 1

with open('patchcount', 'w', encoding='utf-8') as file:
	file.write(str(patchcount))

# Setting up a merging container
CockDB = ET.Element('cockatrice_carddatabase', attrib={'version': '4'})
setdata = ET.Element('sets')
CockDB.append(setdata)
carddata = ET.Element('cards')
CockDB.append(carddata)

# Merging files
for xfile in setFilesDir.glob('*.xml'):
	print('File found:', xfile.name)
	if not xfile.name in FILEIGNORE:
		try:
			with open(xfile, 'r', encoding='utf-8') as file:
				cdb = ET.parse(file).getroot()
				set_info = cdb.find('sets').find('set')

				setdata.append(set_info)

				card_info = cdb.find('cards')
				for card in card_info.findall('card'):
					carddata.append(card)

				print('Tokens for ', set_info.find('name').text, 'set were merged')
		except FileNotFoundError:
			continue

mergedFilePath = setFilesDir / 'Ascention.xml'
tree = ET.ElementTree(CockDB)
tree.write(mergedFilePath, encoding='utf-8', xml_declaration=True)

print('Press ENTER to finish merging...')
_ = input()
