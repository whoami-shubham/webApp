from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	try:
	    if self.path.endswith("/menu"):
		self.send_response(200)
		self.send_header('Content-type','text/html')
	        self.end_headers()
                menui  = session.query(MenuItem).all()
	        res = ""
                res += '<html><body><h1 style="font-size:32px;text-align:center">Menu-Items</h1>' 
                res += '<table align="center" border="1" style="margin-left:30%;width:40%">'
	        for i in menui:
                    res += '<tr><td style="font-size:20px;text-align:center;background-color:black;color:green"> %s <br> Price : %s <br><a href="/menu/%s/edit">Edit</a><br><a href="#">Delete</a><br> <br></td></tr>' %( i.name ,i.price,i.id)
	        res += '</table></body></html>'
	        self.wfile.write(res)
	        return
            if self.path.endswith("/edit"):
                iD = self.path.split('/')[2]
                if session.query(Restaurant).filter_by(id=iD):
                    self.send_response(200)
                    self.send_header( 'Content-type','text/html')
                    self.end_headers()
                    res=""
                    res += '<html><body>'
                    res += '<form method="POST" enctype="multipart/form-data">'
                    res += '<input type="text" name="update"> &nbsp; '
                    res += '<input type="submit" value="Update"></form>'
                    res += '</body></html>'
                    self.wfile.write(res)
                    return

	    if self.path.endswith("/restaurants"):
	        self.send_response(200)
	        self.send_header('Content-type','text/html')
	        self.end_headers()
                items = session.query(Restaurant).all()
	        res = ""
	        res +='<h1 style="font-size:32px;text-align:center">Restaurants</h1>'
	        res += '<p style="text-align:center"><a href="/restaurants/new" style="text-align:center;font-size:28px">Add new Restaurant </a></p><br><br>'
                res += '<table style="width:40%;margin-left:30%">'
	        for j in items:
		    res += '<tr><td style="color:green;background-color:black;font-size:20px;text-align:center" > %s <br><a href="/restaurants/%s/edit">Edit</a><br><a href="/restaurants/%s/delete">Delete</a><br><br></td></tr>' % (j.name, j.id, j.id)
		res += '</table>'
	        self.wfile.write(res)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                res=""
                res +='<html><body>'
                res +='<form method="POST" enctype="multipart/form-data">'
                res +='<input type="text" name="newr">'
                res +='<input type="submit" value="Create">'
                res +='</form></body></html>'
                self.wfile.write(res)
                return
            if self.path.endswith("/delete"):
                iD = self.path.split('/')[2]
                if session.query(Restaurant).filter_by(id=iD).first():
               	    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    res=""
                    res +='<html><body>'
                    res +='<form method="POST" enctype="multipart/form-data">'
                    res +='<h1>Do you Really want to Delete ?</h1>'      
                    res +='<input type="submit" name="y" value="Yes" >&nbsp; <input type="submit" name="n" value="No">'
                    res +='</form></body></html>'
                    self.wfile.write(res)
                    return				

      

	except IOError:
	    err =""
	    err +="<h1>Error: 404 File Not Found </h1>"
	    self.wfile.write(err) 
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
	        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
	        if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
	            m = fields.get('newr')
                    New = session.query(Restaurant).filter_by(name = m[0]).first()
                    if not New:    
                        rest = Restaurant(name = m[0])
                        session.add(rest)
                        session.commit()
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return
            if self.path.endswith("/edit"):
	        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
	        if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
	            m = fields.get('update')
                    iD = self.path.split('/')[2]
                    New = session.query(Restaurant).filter_by(id = iD).first()
                    New.name = m[0]
                    session.add(New)
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return
                
                   
            if self.path.endswith("/delete"):
	        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
	        if ctype == 'multipart/form-data':
		    fields=cgi.parse_multipart(self.rfile,pdict)
		    true = fields.get('y')
                    if true:
                        iD = self.path.split('/')[2]
                        r = session.query(Restaurant).filter_by(id=iD).first()
                        if r:
                            session.delete(r)
                            session.commit()
                        
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return
        except Exception, e:
            raise e

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print 'server is Running on port %s' % port
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C KeyboardInterrupt'
        server.socket.close()
 





if __name__ == '__main__':
        main()


