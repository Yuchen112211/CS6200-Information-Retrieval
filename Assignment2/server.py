import BaseHTTPServer
from InputParser import inputParser

from io import BytesIO

parser = inputParser()
previousFiles = set([])

class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):
	def do_GET( self ):
		if self.path.startswith("/getData") :
			self.do_parse()
		else:
			self.send_response(200)
			self.send_header( 'Content-type', 'text/html' )
			self.end_headers()
			self.wfile.write( open('index.html', 'r').read() )
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

		body = self.rfile.read(content_length)
		index = body.index('filename')
		fileName = body[index:index+20].split('=')[1].split('\"')[1]
		firstIndex = 0
		for i in range(len(body)):
			if body[i] == '<':
				firstIndex = i
				break
		lastIndex = 0
		for i in range(len(body)-1,-1,-1):
			if body[i] == '>':
				lastIndex = i
				break
		body = body[firstIndex:lastIndex+1]

		self.end_headers()

		response = BytesIO()
		response.write(body)
		global previousFiles

		self.wfile.write(open('index.html', 'r').read() )

		if fileName not in previousFiles:
			parser.getString(response.getvalue())
		else:
			self.wfile.write('<h3>File ' + fileName + ' has already been processed.</h3>')
		
		rst = parser.getAppear()
		freqs = parser.getFreq()

		
		if previousFiles:
			self.wfile.write('<h3>Previous processed file:' + ', '.join(previousFiles) + '</h3>')
		self.wfile.write('<h2>After processing file:' + fileName + '</h2>')
		previousFiles.add(fileName)
		self.wfile.write('<div>')

		for key in rst:
			content = rst[key]
			self.wfile.write('<li>' + str(key) + ':' )
			contentString = ''
			for k in content:
				contentString += str(k)
				contentString += '-'
				contentString += str(freqs[(key,k)])
				contentString += ', '
			self.wfile.write(contentString + '</li>')
		self.wfile.write('</div>')
		self.wfile.write('</body></html>')




httpd = BaseHTTPServer.HTTPServer( ('127.0.0.1', 8000), Handler )
httpd.serve_forever()