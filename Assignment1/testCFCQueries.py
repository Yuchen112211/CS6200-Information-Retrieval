from xml.etree.ElementTree import re
from collections import defaultdict
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

import Ranking
import InputParser


class query(object):
	def __init__(self, root=None):
		self.items = {}
		self.text = ''
		self.ID = -1
		self.result = -1
		self.ranked = []
		if not root:
			return
		for node in root.getiterator():
			if node.tag == "QueryNumber":
				self.ID = int(node.text)
			elif node.tag == "QueryText":
				self.text = node.text
			elif node.tag == "Results":
				self.result = int(node.text)
			elif node.tag == "Item":
				self.items[str(int(node.attrib['score']))] = int(node.text)
		self.ranked = sorted(zip(self.items.keys(), self.items.values()), key = lambda x:-x[1])

	def readFromString(self, s):
		self.text = s

def formQueries():
	file = open('/Users/macbookair11/Downloads/cfc-xml/cfquery.xml', 'r')
	rawInput = file.read()
	file.close()

	root = ET.fromstring(rawInput)

	queries = []

	for i in root:
		t = query(i)
		queries.append(t)

	return queries

def getRankScores(rank, query):
	rank.parseQuery(query.text)
	rank.computeMatrix()

	scores = rank.getScores()
	returnScore = sorted(zip(scores.keys(), scores.values()), key=lambda x:-x[1])
	return returnScore

def precision(query, returnScore, k):
	cnt = 0
	for i in range(k):
		if returnScore[i][0] in query.items:
			cnt += 1
	return float(cnt) / k

# def overallAveragePrecision(rank, queries, k):
# 	cnt = 0
# 	for query in queries:
# 		cnt += precision(rank, query, k)
# 	return cnt / len(queries)

def averagePrecision(query, returnScore, k):
	index = 0
	rst = []
	cnt = 0
	for i in range(k):
		if returnScore[i][0] in query.items:
			cnt += 1
		rst.append(float(cnt) / (i + 1))
	return float(sum(rst)) / k

def precisionRecall(query, returnScore):
	cnt = 0

	relevantNum = -1
	for l in range(len(returnScore)):
		i,k = returnScore[l]
		if k == 0:
			relevantNum = l
			break
	return float(len(query.items)) / relevantNum

def drawPictures():
	rank = Ranking.ranking()
	rank.loadAll()
	queries = formQueries()
	result = defaultdict(list)
	for query in queries:
		score = getRankScores(rank, query)
		result['queryID'].append(query.ID)
		result['precision'].append(precision(query, score, 10))
		result['averagePrecision'].append(averagePrecision(query, score, 10))
		result['precisionRecall'].append(precisionRecall(query, score))

	plt.plot(result['queryID'], result['precision'],'ro', label="Precision")

	plt.plot(result['queryID'], result['averagePrecision'],'bo', label="averagePrecision")

	plt.plot(result['queryID'], result['precisionRecall'],'yo', label="precisionRecall")

	plt.axis([0, len(result['queryID']), 0, 0.6])
	plt.xlabel('Query ID')
	plt.ylabel('Value')
	plt.legend()

	plt.savefig('rst.png')
	plt.show()

	#return result
if __name__ == '__main__':
	rst = drawPictures()
