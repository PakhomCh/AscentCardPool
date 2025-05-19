from pathlib import Path
import json
from datetime import date

# Blacklist for .json files
FILEIGNORE = ['AllCards.json', 'Ascention.json']

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
merged = {}
merged['meta'] = {'date': today, 'version': '7.0.' + str(patchcount)}
merged['data'] = {}

# Merging files
for jfile in setFilesDir.glob('*.json'):
	print('File found:', jfile.name)
	if not jfile.name in FILEIGNORE:
		try:
			with open(jfile, 'r', encoding='utf-8') as file:
				setfile = json.load(file)
		except FileNotFoundError:
			continue

		for key in setfile['data'].keys():
			merged['data'][key] = setfile['data'][key]

mergedFilePath = setFilesDir / 'Ascention.json'

with open(mergedFilePath, 'w', encoding='utf-8') as file:
	json.dump(merged, file, indent=4, ensure_ascii=False)

print('Following sets merged:', *[setcode for setcode in merged['data'].keys()], sep='\n - ')
print('Press ENTER to finish merging...')
_ = input()
