"""
for update
  1. find entry 
  2. reset value
  3. session.add()
  4. session.commit()

 """
								
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant , MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
rename = session.query(Restaurant).filter_by(name="food panda").first()
if rename :
	rename.name ="food gandu"
	session.add(rename)
	session.commit()
else:
	print "that thing doesn't found "

print 'changes made '