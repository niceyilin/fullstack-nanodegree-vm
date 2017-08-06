from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

veggieBugers = session.query(MenuItem).filter_by(name="Veggie Burger")

print "All Veggie Burgers :\n"
for veggieBuger in veggieBugers:
	print veggieBuger.id, ",", veggieBuger.restaurant.name, ", ", veggieBuger.price

urbanVeggieBurger = session.query(MenuItem).filter_by(id = 1).one()

print "Old Urban Veggie Burgers price : ", urbanVeggieBurger.price

urbanVeggieBurger.price = '$2.98'

session.add(urbanVeggieBurger)

session.commit()

urbanVeggieBurger = session.query(MenuItem).filter_by(id = 1).one()

print "New Urban Veggie Burgers price : ", urbanVeggieBurger.price,