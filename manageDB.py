"""
For creating and updating the counting channel message database
"""
import os
import sqlite3
from sqlite3 import Error

import discord

import extract

def name(ctx):
    return f"database/{ctx.guild}_{ctx.channel}.db"

def getLastEntry(con, cur):
    """
    Gets latest entry in database as tuple.
    """
    pass

def update(ctx, con, cur, overlap=100):
    """
    Retrieves up to overlap previous messages from before latest entry, and
    any new messages sent since then.
    Updates database entries accordingly.
    """
    pass

def delete(filepath):
    try:
        os.remove(filepath)
    except OSError:
        return "failure"
    return "success"

async def rebuild(ctx, con, cur):
    """
    Pulls ENTIRE history of channel and re-processes. Replaces duplicates.
    Will take a long time.
    """
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

    # Get messages from channel the command was sent in
    channel = ctx.channel
    inserter = """INSERT INTO messages (id, author, created_timestamp, content)
        VALUES (?, ?, ?, ?);"""
    clist = []
    async for message in channel.history(limit=10, oldest_first=True):
        print("hi")
        created_timestamp = message.created_at.timestamp()
        clist.append(message.id, message.author, created_timestamp, message.content)
    print(clist)
