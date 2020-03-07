from xml.etree.ElementTree import re
from collections import defaultdict
import xml.etree.ElementTree as ET

class article(object):

	def __init__(self, rawInput):

		self.parsed = False

		root = ET.fromstring(rawInput)

		rawInputLines = rawInput.split('\n')
		combineString = [rawInputLines[0].split(' ')[-1]]

		pattern = '[\\s.,!?:;()<>/=+\"\[\]-]+'

		self.datas = {}

		for record in root:
			keyTrees = record.getiterator()
			currentString = ''
			recordNum = -1
			for key in keyTrees:
				if key.tag == 'RECORDNUM':
					recordNum = int(key.text)
				else:
					text = key.text
					if not text:
						continue
					currentString += (' '.join(re.split(pattern,key.text)))
			self.datas[recordNum] = currentString


		# for line in rawInputLines[1:]:
		# 	if line[:2] == '  ':
		# 		combineString[-1] += ' '.join(re.split(pattern,line[1:]))
		# 	else:
		# 		keys.append(line[:2])
		# 		currentStringList = re.split(pattern,line[2:])
		# 		currentString = ' '.join(currentStringList)
		# 		combineString.append(currentString)


	def provideWords(self):

		return [i.strip(' !@#$%^&*();:,.?/~`') for i in (' '.join(self.datas.values())).split(' ')]

	def getPaperNumber(self):

		return self.datas['PN']

	def getRecordNumber(self):
		if 'RECORDNUM' not in self.datas:
			return -2
		if 'REFERENCES' not in self.datas:
			return -1
		return self.datas['RECORDNUM']
		
if __name__ == '__main__':
	file = '/Users/macbookair11/Downloads/cfc-xml/cf74.xml'
	data = open(file,'r').read()
	aa = article(data)
	print aa.datas[3]


