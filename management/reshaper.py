from pathlib import Path
import json
from datetime import date

# Finding out the TODAY date in DD-MM-YYYY format
today = date.today().strftime('%d-%m-%Y') # Пример: '19-05-2025'

# Getting set files directory
setFilesDir = Path(__file__).parent.parent / 'data'
setFilesDir.mkdir(exist_ok=True)

try:
	with open(setFilesDir / 'Ascention.json', 'r', encoding='utf-8') as file:
		setsfile = json.load(file)
except FileNotFoundError:
	setsfile = {}

# Setting up a card data container
reshaped = {}
reshaped['meta'] = setsfile['meta']
reshaped['data'] = {}

for set in setsfile['data']:
	for card in setsfile['data'][set]['cards']:
		if not card['name'] in reshaped['data']:
		
			reshaped['data'][card['name']] = card

			if type(reshaped['data'][card['name']]['setCode']) == str:
				reshaped['data'][card['name']]['setCode'] = [card['setCode']]

		elif not card['setCode'] in reshaped['data'][card['name']]['setCode']:
			reshaped['data'][card['name']]['setCode'].append(card['setCode'])

with open(setFilesDir / 'AllCards.json', 'w', encoding='utf-8') as file:
	json.dump(reshaped, file, indent=4, ensure_ascii=False)

print(len(reshaped['data']), 'cards reshaped.')
print('Press ENTER to finish reshaping...')
_ = input()
