#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach 

#fake DB using only a list, 
#in this way, data is stored in cache, so it will be lost everytime web server is reboot
#DB = []  

## Get posts from database.
def GetAllPosts():
	DB = psycopg2.connect("dbname = forum")
	cur = DB.cursor()	
	query = "SELECT time, content FROM posts ORDER BY time DESC"
	cur.execute(query)	
	posts = cur.fetchall()
	postlist = []

	for post in posts:
		# try to avoid JS atack
		# the txt is treated string by database and web server, 
		# so it will be stored in db as normal, but when it's requested by user/browser
		# it is treated as javascript code by the web brower and run to cause bad effect
		# e.g. <h2 style="color: #FF6699; font-family: Comic Sans MS">Spam, spam, spam, spam,<br>Wonderful spam, glorious spam!</h2>
		postlist.append({'content' : str(bleach.clean(post[1])), 'time' : post[0]}) 		
	DB.close()

	return postlist

## Add a post to the database.
def AddPost(content):
	'''Add a new post to the database.
	
	Args:
	content: The text content of the new post.
	'''
	#t = time.strftime('%c', time.localtime())
	#DB.append((t, content))
	
	DB = psycopg2.connect("dbname = forum")
	cur = DB.cursor()
	
	# try to avoid Security hole: 
	# if content include quote like "can't", below way is safe solution : 
	# use query parameters instead of string substition
	#cur.execute("INSERT INTO posts (content) values ('%s')" % content) wrong
	SQL = "INSERT INTO posts (content) values (%s)"
	data = (content,) # python tuple
	cur.execute(SQL, data)
	DB.commit()
	
	DB.close()