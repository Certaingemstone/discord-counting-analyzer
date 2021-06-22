import sqlite3

con = sqlite3.connect(r"database/test.db")
cur = con.cursor()

# Create table if not already there
createifndef = """
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    author TEXT NOT NULL,
    created_timestamp INTEGER NOT NULL,
    edited_timestamp INTEGER,
    content TEXT NOT NULL,
    number INTEGER,
    error INTEGER,
    length INTEGER
    );"""
cur.execute(createifndef)

inserter = """INSERT INTO messages (id, author, created_timestamp, content)
    VALUES (?, ?, ?, ?)"""
cur.execute(inserter, (6, "Jade", 1109120308, "This is a test message"))
cur.execute(inserter, (7, "Jade", 1109120310, "This is a second test message"))

# Finalize changes
con.commit()
