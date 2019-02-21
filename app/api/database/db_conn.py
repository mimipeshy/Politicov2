"""
Create database tables
"""
import os

import psycopg2
import psycopg2.extras
from flask import current_app


def dbconn():
    """
    ccnnect to the main database
    """
    try:
        connection = psycopg2.connect(dbname='politico', user='peshy', host='localhost', password='admin')
        return connection
    except psycopg2.DatabaseError as e:
        return {'error': str(e)}


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

        cursor.close()
        connection.commit()
        connection.close()

    except psycopg2.DatabaseError as e:
        print(e)


def drop_tables():
    db_test_url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(db_test_url)
    cursor = connection.cursor()
    users = """DROP TABLE IF EXISTS users CASCADE"""
    blacklist = """DROP TABLE IF EXISTS blacklist CASCADE"""
    party = """DROP TABLE IF EXISTS party CASCADE"""
    office = """DROP TABLE IF EXISTS office CASCADE"""
    votes= """DROP TABLE IF EXISTS votes CASCADE"""
    queries = [users, blacklist, party, office, votes]
    try:
        for query in queries:
            cursor.execute(query)

        connection.commit()
        connection.close()
    except psycopg2.DatabaseError as e:
        print(e)
