#title, release_date, watched
import datetime
import sqlite3
from sqlite3.dbapi2 import Cursor


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?, 0);"
INSERT_USERS = "INSERT INTO users (username) VALUES (?)"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watchername = ?; "
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?)"

connection = sqlite3.connect("data.db")

def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_USERS_TABLE)
    pass

def add_user(username):
    with connection:
        connection.execute(INSERT_USERS, (username,))

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

def watch_movie(username, movie_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
    pass

def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()
