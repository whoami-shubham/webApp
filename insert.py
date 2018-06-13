from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

rest1 = Restaurant(id = 2, name="food pandu")
session.add(rest1)
session.commit()

menuitem1 = MenuItem(id = 2, name = "maggi", description="patanjali noodles", course="entree", price="10 $",restaurant_id=2, restaurant=rest1 )
session.add(menuitem1)
session.commit()

print 'value added'