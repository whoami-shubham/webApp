from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

items = session.query(Restaurant).all()

print 'Restaurants :'
for i in items:
	print i.name

menu = session.query(MenuItem).all()
print 'MenuItems :'
for j in menu:
	print j.name