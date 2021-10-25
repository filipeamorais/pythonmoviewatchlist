#title, release_date, watched
import datetime
import sqlite3
from sqlite3.dbapi2 import Cursor


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
    );"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    watchername TEXT,
    title TEXT
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp, watched) VALUES (?, ?, 0);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watchername = ?; "
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?"
INSERT_WATCHLIST = "INSERT INTO watched (watchername, title) VALUES (?, ?)"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"

connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)
    pass

def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES,(title, release_timestamp))
    pass

def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor() #(moraisf) using cursor since it has multiple values
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()

def watch_movie(username, title):
    with connection:
        cursor = connection.cursor()
        cursor.execute(DELETE_MOVIE, (title,))
        cursor.execute(INSERT_WATCHLIST, (username, title))
    pass

def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()
