
-- intial database setup file, to be run as psql > \i tournament.sql

-- Table definitions for the tournament project.
-- create database tournament;

-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
create table players (id  serial primary key,
					  name text);

create table matches (id serial primary key,
						winNums serial, 
						gamesNums serial);

-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


