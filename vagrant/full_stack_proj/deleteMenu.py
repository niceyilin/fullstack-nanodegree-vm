from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

spinachIceCreams = session.query(MenuItem).filter_by(name = "Spinach Ice Cream")
print "Previously these was ", spinachIceCreams.count(), "Spinach Ice Cream"

for spinachIceCream in spinachIceCreams:
	print 'deleting Spinach Ice Cream from Restaurant "', spinachIceCream.restaurant.name, '"'
	session.delete(spinachIceCream)
	session.commit()


spinachIceCreams = session.query(MenuItem).filter_by(name = "Spinach Ice Cream")
print "Now these is ", spinachIceCreams.count(), "Spinach Ice Cream"