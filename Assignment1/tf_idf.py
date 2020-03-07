import math

#This should only be an API for the InputParser to get the Term's value
#Should be EASY
#Steps:1 get the term frequency. 2 get the inverse document frequency.
class tf_idf(object):

	def __init__(self):
		pass

	# Pass a InputParser object to compute the value of a term and a document.
	# The score belongs to the document.
	def computeDoc(self, IP, term, docID):
		wordAppearance = IP.getAppear()
		wordFrequency = IP.getFreq()
		if wordFrequency[(term, docID)] == 0:
			return 0


		tf = float(wordFrequency[(term, docID)]) / float(IP.getDocWordNum(docID))
		df = len(wordAppearance[term])
		N  = IP.getDocNum()

		# The weight is log(1+tf)/log(N/df)
		# N is the total number of docs

		if df == 0 or df == N:
			return 0
		else:
			# if float(math.log(float(N) / float(df), 10)) == 0:
			# 	print term, N, df, math.log(float(N) / float(df), 10)
			# 	input('')
			score = math.log(1 + float(tf)) / math.log(float(N) / float(df), 10)
			return score * 100

	def computeQuery(self, IP, term, queryWords):
		queryLength = len(queryWords)
		wordAppearance = IP.getAppear()
		wordFrequency = IP.getFreq()


		tf = float(queryWords.count(term)) / float(queryLength)
		df = len(wordAppearance[term])
		N = IP.getDocNum()
		if df == 0 or df == N:
			return 0
		else:
			# if float(math.log(float(N) / float(df), 10)) == 0:
			# 	print term, N, df, math.log(float(N) / float(df), 10)
			# 	input('')
			score = math.log(1 + float(tf)) / math.log(float(N) / float(df), 10)
			return score * 100

if __name__ == '__main__':
	import InputParser
	IP = InputParser.inputParser()
	file = open('/Users/macbookair11/Downloads/cfc-xml/cf74.xml', 'r')
	data = file.read()
	file.close()
	IP.getString(data)

	TF_IDF = tf_idf()
	print IP.getDocNum(),IP.getDocWordNum('120')

