"""
For creating and updating the counting channel message database
"""

import sqlite3
import discord

import extract

def getLastEntry(con, cur):
    pass

def rebuild(con, cur):
    """
    Wipes any existing data, pulls entire history of channel and re-processes.
    Will take a long time.
    """

def update(con, cur):
    pass
