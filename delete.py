from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

print 'enter name of restaurant to delete'

res = input()

d = session.query(Restaurant).filter_by(name=res).first()
if d:
    session.delete(d)
    session.commit()
    print 'Deleted !'
else:
    print 'No such Restaurant Exists'
