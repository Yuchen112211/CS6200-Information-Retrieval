from xml.etree.ElementTree import re

class article(object):

	def __init__(self, rawInput):

		self.parsed = False
		rawInput = rawInput.strip()
		rawInputLines = rawInput.split('\n')
		combineString = [rawInputLines[0].split(' ')[-1]]
		keys = ['PN']

		pattern = '[\\s.,!?:;()<>/=+\"\[\]-]+'

		for line in rawInputLines[1:]:
			if line[:2] == '  ':
				combineString[-1] += ' '.join(re.split(pattern,line[1:]))
			else:
				keys.append(line[:2])
				currentStringList = re.split(pattern,line[2:])
				currentString = ' '.join(currentStringList)
				combineString.append(currentString)

		self.datas = {}
		for i in range(len(keys)):
			self.datas[keys[i]] = combineString[i]


	def provideWords(self):

		return [i.strip(' !@#$%^&*();:,.?/~`') for i in (' '.join(self.datas.values())).split(' ')]

	def getPaperNumber(self):

		return self.datas['PN']

	def getRecordNumber(self):
		if 'RF' not in self.datas:
			return -2
		if 'RN' not in self.datas:
			return -1
		return self.datas['RN']
		