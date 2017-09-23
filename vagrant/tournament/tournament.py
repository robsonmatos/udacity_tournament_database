#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import re


def connect(database_name):
    """Connect to the PostgreSQL database. Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)

def send_query(query, params=()):
    """Query the tournament database."""
    res = []
    
    db = connect("tournament")
    c = db.cursor()
    c.execute(query, params)
    if re.search("^SELECT", query):
        res = c.fetchall()
    else:
        db.commit()
    db.close()
    return res

def deleteMatches():
    """Remove all the match records from the database."""
    send_query("DELETE FROM matches;")

def deletePlayers():
    """Remove all the player records from the database."""
    send_query("DELETE FROM players;")

def countPlayers():
    """Returns the number of players currently registered."""
    ids = send_query("SELECT COUNT(*) FROM players GROUP BY player_id;")
    return len(ids)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    send_query("INSERT INTO players (name) VALUES (%s)", (bleach.clean(name), ))

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
    standings = send_query("SELECT * FROM standings;")
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    send_query("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);", (winner, loser)) 
 
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
    players = send_query("SELECT * FROM wins ORDER BY num_wins DESC;")

    pairings = []
    idx = 0
    while idx < len(players):
        pairings.append((players[idx][0], players[idx][1], 
            players[idx+1][0], players[idx+1][1]))
        idx += 2
    return pairings
