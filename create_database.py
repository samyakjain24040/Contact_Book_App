"""
This script creates a MySQL database named 'contact_book'.
"""

# Import the required module
import mysql.connector

# Establish a connection to MySQL
myDB = mysql.connector.connect(
    host="localhost",  # Host name
    user="root",  # User name
    password=""  # Password
)

# Create a cursor object to interact with the database
myCursor = myDB.cursor()

# Create the database
myCursor.execute("CREATE DATABASE contact_book")
myCursor.execute("create database contact_book")
