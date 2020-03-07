import BaseHTTPServer
from InputParser import inputParser

from io import BytesIO

import Ranking, testCFCQueries

parser = inputParser()

class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):
	def do_GET( self ):
		self.send_response(200)
		self.send_header( 'Content-type', 'text/html' )
		self.end_headers()
		self.wfile.write( open('indexRank.html', 'r').read() )
		self.wfile.write('</body></html')

	def do_parse(self):
		self.send_response(200)
		self.send_header( 'Content-type', 'text/html' )
		self.end_headers()
		self.wfile.write( "Only for test function." )

	def do_POST(self):
		self.send_response(200)
		self.send_header( 'Content-type', 'text/html' )
		content_length = int(self.headers.getheader('Content-Length'))

		body = self.rfile.read(content_length).split('\r\n')

		text = body[3]
		query = testCFCQueries.query()
		query.readFromString(text)

		rank = Ranking.ranking()
		rank.loadAll()
		scores = testCFCQueries.getRankScores(rank, query)
		relevantFiles = []
		for i in range(min(20, len(scores))):
			if scores[i][1] == 0:
				break
			else:
				relevantFiles.append(scores[i][0])

		self.end_headers()
		self.wfile.write('<div></h2>Your Query: ' + text + "</h2>")
		if not relevantFiles:
			self.wfile.write('<h3>Sorry, there is no match for your query.</h3>')
		else:
			self.wfile.write('<h3>Search Results(At most 20):</h3>')
			for file in relevantFiles:
				self.wfile.write("<div>File ID: " + file)
				self.wfile.write("<li>")
				self.wfile.write(rank.IP.docText[file] + "</li></div><hr>")
		self.wfile.write('</div></body></html>')

httpd = BaseHTTPServer.HTTPServer( ('127.0.0.1', 8000), Handler )
httpd.serve_forever()
'''
Can one distinguish between the effects of mucus hypersecretion and infection on the submucosal glands of the respiratory tract in CF?
'''