import mysql.connector

# Establish connection to the MySQL database
myDB = mysql.connector.connect(
    host="localhost", # Host name
    user="root", # User name
    password="", # Password
    database="contact_book" # Database name
)

# Create a cursor object to interact with the database
myCursor = myDB.cursor()

# Create a table called 'contacts' with the specified columns
myCursor.execute("CREATE TABLE contacts ( \
    Name varchar(255) NOT NULL, \
    Number INT NOT NULL PRIMARY KEY, \
    Email VARCHAR(255) NOT NULL, \
    Address VARCHAR(255) NOT NULL \
    )")

