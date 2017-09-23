-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT,
	wins INT);

CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	player_a SERIAL REFERENCES players(id),
	player_b SERIAL REFERENCES players(id),
	CONSTRAINT dup_player CHECK (player_a <> player_b));

CREATE VIEW standings AS
	SELECT players.id, players.name, players.wins, count(matches.id) 
	FROM players LEFT JOIN matches 
	ON players.id=matches.player_a 
	OR players.id=matches.player_b
	GROUP BY players.id, players.name, players.wins
	ORDER BY count(matches.id);