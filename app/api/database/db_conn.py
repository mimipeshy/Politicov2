"""
Create database tables
"""
import os

import psycopg2
import psycopg2.extras
from flask import current_app
from sys import modules

def dbconn():
    """
    ccnnect to the main database
    """
    connection = None
    try:
        if 'pytest' in modules:
            db = 'test_andela'
        else:
            db='politico'
        connection = psycopg2.connect(dbname=db, user='postgres', host='localhost', password='admin')
    except psycopg2.DatabaseError as e:
        try:
            if os.getenv('CONFIG_SETTING') == 'production':
                connection = psycopg2.connect(os.environ['DATABASE_URL'],
                                              sslmode='require')
        except:
            print('connection failed')
            return {'error': str(e)}
    connection.autocommit = True
    return connection

def create_tables():
    """
    Create tables for the database
    """
    queries = (
        """
        CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY NOT NULL,
                fname VARCHAR (80) NOT NULL,
                lname VARCHAR (80) NOT NULL,
                othername VARCHAR (80),
                email VARCHAR(80) NOT NULL UNIQUE,
                phone VARCHAR (24) NOT NULL,  
                password VARCHAR(255) NOT NULL,
                passUrl VARCHAR(255) NOT NULL,
                is_admin BOOLEAN
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS party (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(80) NOT NULL UNIQUE,
            hqAddress VARCHAR(150) NOT NULL,
            logoUrl VARCHAR(80) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS office (
        office_id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(80) NOT NULL UNIQUE,
        type VARCHAR(80) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS votes (
        id SERIAL,
        office INTEGER,
        candidate INTEGER,
        voter INTEGER,
        PRIMARY KEY (office, voter)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS candidate(
         id SERIAL,
         candidate INTEGER,
         office INTEGER,
         PRIMARY KEY (office, candidate)      
        )
        """
    )
    try:
        connection = dbconn()
        cursor = connection.cursor()
        # create tables
        for query in queries:
            cursor.execute(query)
        connection.commit()
        connection.close()

    except psycopg2.DatabaseError as e:
        print(e)


def drop_tables():
    connection = dbconn()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT table_schema,table_name FROM information_schema.tables "
        " WHERE table_schema = 'public' ORDER BY table_schema,table_name"
    )
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("drop table "+row[1] + " cascade")
    connection.commit()
    connection.close()
