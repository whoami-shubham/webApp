from BaseHTTPServer import BaseHTTPRequestHandler , HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	"""docstring for webserverHandler"""
	def do_GET(self):
		try:
		    if self.path.endswith("/hello"):
		    	self.send_response(200)
		    	self.send_header('Content-type','text/html')
		    	self.end_headers()
		    	res = ""
		    	res += "<html><body>"
		    	res +="<h1>Hello !</h1>"
		    	res += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say ? </h2><input name='message' type='text' ><input type='submit' value='Submit'></form></body></html>"
		    	self.wfile.write(res)
		    	return
		    if self.path.endswith("/hi"):
		    	self.send_response(200)
		    	self.send_header('Content-type','text/html')
		    	self.end_headers()
		    	res = ""
		    	res += "<html><body>"
		    	res +="<h1>Hey Hi !</h1>"
		    	res += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say ? </h2><input name='message' type='text' ><input type='submit' value='Submit'></form></body></html>"
		    	self.wfile.write(res)
		    	return
		    if self.path.endswith(""):
		    	self.send_response(200)
		    	self.send_header('Content-type','text/html')
		    	self.end_headers()
		    	res = ""
		    	res +="<h1>Home</h1>"
		    	self.wfile.write(res)
		    	return

		except IOError:
			err =""
			err +="<h1>Error: 404 File Not Found </h1>"
			self.wfile.write(err)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()
			ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile,pdict)
				messagecontent = fields.get('message')
			output =""
			output += "<html><body>"
			output += " <h2> Okay , How about this : </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say ? </h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
			output +="</body></html>"
			self.wfile.write(output)


		except Exception, e:
			raise e


			
		

def main():
	try:
	    port = 8080
	    server = HTTPServer(('',port),webserverHandler)
	    print "web server running on port %s" %port
	    server.serve_forever()

	except KeyboardInterrupt:
		print "^C KeyboardInterrupt "
		server.socket.close()



if __name__ == '__main__':
	main()