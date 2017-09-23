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
	player_id SERIAL PRIMARY KEY,
	name TEXT);

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	winner_id SERIAL REFERENCES players(player_id),
	loser_id SERIAL REFERENCES players(player_id),
	CONSTRAINT duplicate CHECK (winner_id<>loser_id));

CREATE VIEW wins AS
	SELECT players.player_id, players.name, COUNT(matches.match_id) AS num_wins
	FROM players 
	LEFT JOIN matches ON players.player_id=matches.winner_id
	GROUP BY players.player_id
	ORDER BY players.player_id;

CREATE VIEW standings AS
	SELECT cnt_matches.player_id, cnt_matches.name, wins.num_wins, cnt_matches.num_matches
	FROM (SELECT players.player_id, players.name, COUNT(matches.match_id) AS num_matches
			FROM players 
			LEFT JOIN matches 
			ON players.player_id=matches.winner_id
			OR players.player_id=matches.loser_id
			GROUP BY players.player_id, players.name) AS cnt_matches
	JOIN wins ON cnt_matches.player_id=wins.player_id;