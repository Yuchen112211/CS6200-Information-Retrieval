import math
from xml.etree.ElementTree import re
from collections import defaultdict

from InputParser import *
import tf_idf

tf_idf_obj = tf_idf.tf_idf()
# The query needs to be vectorized, tf of query is only based on the query
# But the idf of the query is based on the whole document.
# Then we need to compute the relationship between the query and each document, then sort it by the score.
# The former InputParse needs to be used, since it is the tokenizer.

# This function should compute the cosine similarity of one doc to the query
# Only a computational function.
def cosine(vector1, vector2):
	# if vector2.count(0) + 1 >= len(vector2):
	# 	return 0
	top = sum([vector1[i] * vector2[i] for i in range(len(vector1))])
	bottom = math.sqrt(sum([pow(i,2) for i in vector1]))
	return float(top) / float(bottom) + (len(vector2) - vector2.count(0)) * 2 if bottom > 0 else 0

# The steps are as follows:
# 1. The InputParser first parse all the files, get all the data.
# 2. Get the query, split it by the pattern that we used in the InputParser and remove the stopwords.
# 3. Compute the tf-idf vector of the query, store it.
# 4. Compute all tf-idf vector of each document, store it.

# 5. Compute all cosine value which would compare the query and document.
# 6. Sort the cosine value decreasingly, then select the top K documents to return.

class ranking(object):
	def __init__(self):
		self.IP = inputParser()
		self.queryWords = []
		self.queryVector = []
		self.docVector = defaultdict(list)
		self.scores = defaultdict(float)
		pass

	def passParser(self, anotherIP):
		self.IP = anotherIP

	def loadAll(self):
		IP = inputParser()
		file = open('/Users/macbookair11/Downloads/cfc-xml/cf74.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		file = open('/Users/macbookair11/Downloads/cfc-xml/cf75.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		file = open('/Users/macbookair11/Downloads/cfc-xml/cf76.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		file = open('/Users/macbookair11/Downloads/cfc-xml/cf77.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		file = open('/Users/macbookair11/Downloads/cfc-xml/cf78.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		file = open('/Users/macbookair11/Downloads/cfc-xml/cf79.xml', 'r')
		data = file.read()
		file.close()
		IP.getString(data)

		self.passParser(IP)

	# Essential, get the words of the query.
	def parseQuery(self, query):
		pattern = '[\\s.,!?:;()<>/=+\"\[\]-]+'
		rst = []
		words = re.split(pattern, query)
		for word in words:
			word = word.lower().strip()
			if word in stopWords:
					continue
			try:
				word = int(word)
				if len(str(word)) == 4 and word >  1800 and word < 2100:
					rst.append(str(word))
			except Exception as e:
				if word:
					rst.append(str(word))
		self.queryWords = rst

	def computeMatrix(self):
		if self.queryWords == []:
			# To be done.
			return
		terms = set(self.queryWords)
		docVector = defaultdict(list)
		queryVector = []
		for term in terms:
			queryVector.append(tf_idf_obj.computeQuery(self.IP, term, self.queryWords))
			for docID in self.IP.getDocID():
				score = tf_idf_obj.computeDoc(self.IP, term, docID)
				docVector[docID].append(score)
		self.queryVector = queryVector
		self.docVector = docVector

	def getScores(self):
		for docID in self.docVector:
			score = cosine(self.queryVector, self.docVector[docID])
			self.scores[docID] = score
		return self.scores



if __name__ == '__main__':
	rank = ranking()

	rank.loadAll()

	query = "What are the effects of calcium on the physical properties of mucus from CF patients? "

	rank.parseQuery(query)

	rank.computeMatrix()

	scores = rank.getScores()

	print scores
