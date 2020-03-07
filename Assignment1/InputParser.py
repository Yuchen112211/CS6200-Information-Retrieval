from xml.etree.ElementTree import re
from collections import defaultdict
import xml.etree.ElementTree as ET

stoplist = ' '.join(open('stoplist.txt', 'r').readlines())
stopWords = set(stoplist.split())

class inputParser(object):
	def __init__(self):
		self.docText = defaultdict(str)
		self.wordAppearance = defaultdict(set)
		self.wordFrequency = defaultdict(int)
		self.docWordNum = defaultdict(int)
		self.docNum = [] 

	def getString(self, rawInput):

		root = ET.fromstring(rawInput)
		rawInputLines = rawInput.split('\n')
		combineString = [rawInputLines[0].split(' ')[-1]]

		pattern = '[\\s.,!?:;()<>/=+\"\[\]-]+'

		datas = {}

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
			self.docNum.append(str(recordNum))
			self.docText[str(recordNum)] = ET.tostring(record, encoding='utf8', method='xml')
			
			datas[recordNum] = currentString

		for num in datas:
			words = re.split(pattern, datas[num])
			for word in words:
				word = word.lower().strip()
				if word in stopWords:
					continue
				try:
					word = int(word)
					if len(str(word)) == 4 and word >  1800 and word < 2100:
						self.wordAppearance[word].add(str(int(num)))

						self.wordFrequency[(word,str(int(num)))] += 1

						self.docWordNum[str(int(num))] += 1
				except Exception as e:
					if word:
						self.wordAppearance[word].add(str(int(num)))

						self.wordFrequency[(word,str(num))] += 1

						self.docWordNum[str(int(num))] += 1

	def getAppear(self):
		return self.wordAppearance

	def getFreq(self):
		return self.wordFrequency

	def getDocNum(self):
		return len(self.docNum)

	def getDocID(self):
		return self.docNum

	def getDocWordNum(self, docID):
		return self.docWordNum[docID]

# if __name__ == '__main__':
# 	obj = inputParser()
# 	obj.getFile('cfc/cf74')
# 	obj.parseAllArticles()
# 	#print obj.printOut()