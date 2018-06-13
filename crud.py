from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant, MenuItem

import cgi
from BaseHTTPServer import BaseHTTPRequestHandler ,HTTPServer


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

items = session.query(Restaurant).all()
menui  = session.query(MenuItem).all()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/menu"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
		    	        self.end_headers()
		    	        res = ""
		    	        res +='<h1 style="font-size:32">Menu-Items</h1>'
		    	        res +='<ol style="font-size:20">'
		    	        for i in menui:
                                    res += '<li> %s </li><p> Price : %s </p><br>' %( i.name ,i.price)
		    	        res += '</ol>'
		    	        self.wfile.write(res)
		    	        return

			if self.path.endswith("/resturant"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
		    	        self.end_headers()
		                res = ""
				res +='<h1 style="font-size:32">Resturants</h1>'
				res += '<ol style="font-size:20">'
				for j in items:
					res += '<li> %s </li><br>' % j.name
				res += '</ol>'
				self.wfile.write(res)
                                return


				

		except IOError:
			err =""
			err +="<h1>Error: 404 File Not Found </h1>"
			self.wfile.write(err)
			



def main():
	try:
		port = 8080
		server = HTTPServer(('',port),webserverHandler)
		print 'server is Running on port %s' %port
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C KeyboardInterrupt'
        server.socket.close()
 






if __name__ == '__main__':
	main()
