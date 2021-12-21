"""
For creating and updating the counting channel message database
"""
import os
import sqlite3
from sqlite3 import Error

import discord

import extract

def countingChannelID(ctx):
    # see if already bound to a channel
    nameFile = f"database/{ctx.guild}.txt"
    if os.path.exists(nameFile):
        with open(nameFile, "r") as file:
            lines = file.readlines()
            ID = int(lines[0])
    else:
        ID = None
    return ID

def databaseName(ctx):
    return f"database/{ctx.guild}.db"

async def update(ctx, con, cur, overlap=100):
    """
    Retrieves up to overlap previous messages from before latest entry, and
    any new messages sent since then.
    Updates database entries accordingly.
    """
    # Figure out where to start the updating
    cur.execute(f"SELECT * FROM messages ORDER BY created_timestamp DESC LIMIT {overlap}")
    hist = cur.fetchmany(overlap)
    startFromID = hist[-1][0]
    # Do the updating
    channel = discord.utils.get(ctx.guild.channels, id=countingChannelID(ctx))
    startFrom = await channel.fetch_message(startFromID)
    upd= """INSERT OR REPLACE INTO messages (id, author, created_timestamp, edited_timestamp, number)
        VALUES (?, ?, ?, ?, ?);"""
    async for message in channel.history(limit=None, oldest_first=True, after=startFrom):
        created_timestamp = message.created_at.timestamp()
        if message.edited_at:
            edited_timestamp = message.edited_at.timestamp()
        else:
            edited_timestamp = -1
        number = await extract.findNumber(str(message.content))
        info = (int(message.id), str(message.author), int(created_timestamp), int(edited_timestamp), int(number))
        cur.execute(upd, info)
    con.commit()
    return str(channel)

def delete(filepath):
    try:
        os.remove(filepath)
    except OSError:
        return "failure"
    return "success"

async def rebuild(ctx, con, cur):
    """
    Pulls ENTIRE history of channel and re-processes. Replaces duplicates.
    """
    # Create table if not already there
    createifndef = """
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        author TEXT NOT NULL,
        created_timestamp INTEGER NOT NULL,
        edited_timestamp INTEGER,
        number INTEGER
        );"""
    cur.execute(createifndef)
    # Get messages from channel the bot is bound to
    channel = discord.utils.get(ctx.guild.channels, id=countingChannelID(ctx))
    inserter = """INSERT OR REPLACE INTO messages (id, author, created_timestamp, edited_timestamp, number)
        VALUES (?, ?, ?, ?, ?);"""
    async for message in channel.history(limit=None, oldest_first=True):
        print("Extracting")
        created_timestamp = message.created_at.timestamp()
        if message.edited_at:
            edited_timestamp = message.edited_at.timestamp()
        else:
            edited_timestamp = -1
        number = await extract.findNumber(str(message.content))
        print("Success")
        info = (int(message.id), str(message.author), int(created_timestamp), int(edited_timestamp), int(number))
        cur.execute(inserter, info)
    con.commit()
    return str(channel)
