import Article

stoplist = ' '.join(open('stoplist.txt', 'r').readlines())
stopWords = set(stoplist.split())

class inputParser(object):
	def __init__(self):
		self.articles = []
		self.wordAppearance = {}
		self.appearTimes = 0 

	def getFile(self, inputPath):
		'''
		The input of the function is a simple file path.
		There's no output, put all the data into self variable.
		'''
		inputFile = ''
		try:
			inputFile = open(inputPath, 'r')
		except Exception as e:
			print ("File path \"%s\" does not exists."%inputPath)
			return
		else:
			pass
		finally:
			pass

		fileData = inputFile.read()
		articleRaw = fileData.split('\nPN ')
		
		for articleText in articleRaw[1:-1]:
			article = Article.article(articleText)
			self.articles.append(article)

	def getString(self, inputs):
		fileData = inputs
		articleRaw = fileData.split('\nPN ')
		
		for articleText in articleRaw:
			article = Article.article(articleText)
			self.articles.append(article)


	def tokenizeWords(self, articleObject):
		'''
		The input of the function is an object of article
		This would be the main function to process the article:
		1. Remove the stop words.
			a) Make the words into list-form, all together, regardless of the keys.
			b) remove all the stop words.
		2. Tokenize
		'''
		words = articleObject.provideWords()
		recordNum = articleObject.getRecordNumber()
		if recordNum == -2:
			return
		if recordNum == -1:
			recordNum = self.appearTimes


		for i, word in enumerate(words):
			word = word.lower().strip()
			if word not in stopWords:
				try:
					word = int(word)
					if len(str(word)) == 4 and word >  1800 and word < 2100:
						if word in self.wordAppearance:
							self.wordAppearance[word].add(str(int(recordNum)) + '-' + str(i))
						else:
							self.wordAppearance[word] = set([str(int(recordNum)) + '-' + str(i)])
				except Exception as e:
					if word:
						if word in self.wordAppearance:
							self.wordAppearance[word].add(str(int(recordNum)) + '-' + str(i))
						else:
							self.wordAppearance[word] = set([str(int(recordNum)) + '-' + str(i)])
		return

	def parseAllArticles(self):
		for i in range(len(self.articles)):
			if not self.articles[i].parsed:
				self.appearTimes += 1
				self.tokenizeWords(self.articles[i])
				self.articles[i].parsed = True

	def printOut(self):
		return [(i,self.wordAppearance[i]) for i in self.wordAppearance]


# if __name__ == '__main__':
# 	obj = inputParser()
# 	obj.getFile('cfc/cf74')
# 	obj.parseAllArticles()
# 	#print obj.printOut()