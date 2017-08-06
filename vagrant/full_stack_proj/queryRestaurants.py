from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
	print "id = ", restaurant.id, ",\t name = ", restaurant.name

menuItems = session.query(MenuItem).all()

for menuItem in menuItems:
	#print "\t-> name: ", menuItem.name, "\t\t\tprice: $", menuItem.price
	print "\t-> name: {0:70}\t price: $ {1}".format(menuItem.name, menuItem.price)

print "...query is done !"