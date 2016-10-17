#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	DB = connect()
	cur = DB.cursor()
	SQL = "UPDATE matches SET winNums = 0"
	cur.execute(SQL)
	SQL = "UPDATE matches SET gamesNums = 0"
	cur.execute(SQL)
	DB.commit()
	DB.close()

def deletePlayers():
	"""Remove all the player records from the database."""
	DB = connect()
	cur = DB.cursor()
	SQL = "DELETE FROM players"
	cur.execute(SQL)
	SQL = "DELETE FROM matches"
	cur.execute(SQL)
	DB.commit()
	DB.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	DB = connect()
	cur = DB.cursor()
	SQL = "SELECT count(*) FROM players"
	cur.execute(SQL)
	rows = cur.fetchone()
	count = rows[0]
	return count
	


def registerPlayer(name):
	"""Adds a player to the tournament database.
	
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
	
	Args:
	name: the player's full name (need not be unique).
	"""
	# get max of existing id
	DB = connect()
	cur = DB.cursor()
	SQL = "SELECT max(id) FROM players"
	cur.execute(SQL)
	rows = cur.fetchone()
	if rows[0] == None:
		maxid = 0
	else:
		maxid = rows[0]
	# insert new player into players table with id = max+1 
	newid = maxid + 1
	SQL = "INSERT INTO players (id, name) VALUES (%s, %s)"
	newdata = (newid, name) 
	cur.execute(SQL, newdata) # safe way to insert, protect quota injection
	# insert new player into matches table with id = max+1 
	SQL = "INSERT INTO matches (id, winNums, gamesNums) VALUES (%s, %s, %s)"
	newdata = (newid, 0, 0) 
	cur.execute(SQL, newdata)
	
	DB.commit()
	cur.close()
	

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.
	
	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.
	
	Returns:
	A list of tuples, each of which contains (id, name, wins, matches):
	id: the player's unique id (assigned by the database)
	name: the player's full name (as registered)
	wins: the number of matches the player has won
	matches: the number of matches the player has played
	"""
	DB = connect()
	cur = DB.cursor()
	SQL = """SELECT players.id, players.name, matches.winNums, matches.gamesNums
				FROM players LEFT JOIN matches
					ON players.id = matches.id
				ORDER BY matches.winNums DESC"""
	cur.execute(SQL)
	rows = cur.fetchall()
	standinglist = []
	for row in rows:
		standinglist.append((row[0], row[1], row[2], row[3]))
	return standinglist


def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.
	
	Args:
	winner:  the id number of the player who won
	loser:  the id number of the player who lost
	"""	
	DB = connect()
	cur = DB.cursor()
	SQL1 = "UPDATE matches SET winNums = winNums+1 WHERE id = {0}".format(winner)
	cur.execute(SQL1)
	SQL2 = "UPDATE matches SET gamesNums = gamesNums + 1 WHERE id = {0}".format(winner)
	cur.execute(SQL2)
	SQL3 = "UPDATE matches SET gamesNums = gamesNums + 1 WHERE id = {0}".format(loser)
	cur.execute(SQL3)
	DB.commit()
	DB.close()
 
 
def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
  
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
  
	Returns:
	A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
	"""
	sortedplayers = playerStandings()
	pairinglist = []
	for player in sortedplayers:
		id = player[0]
		name = player[1]
		
		if len(pairinglist) == 0:
			pairinglist.append((id, name))
		elif len(pairinglist[-1]) == 2 :  # last pair still missing one player
			pairinglist[-1] += (id, name) 
		else :  # last pair has 2 players already, put this player into a new pair
			pairinglist.append((id, name))
		
	return pairinglist
	
	
	
	
	