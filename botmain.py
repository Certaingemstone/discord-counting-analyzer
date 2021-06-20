#!/usr/bin/env python
"""
Discord bot for counting chat analysis. WIP.
"""

from os import getenv
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv
#import numpy as np
#import matplotlib.pyplot as plt

import manageDB as db
import extract

### Get environment variables ###
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
PREFIX = getenv("PREFIX")
MANAGER = getenv("MANAGER_ID")

### Bot client and database initialization ###
bot = commands.Bot(command_prefix=PREFIX)

### Checks ###
async def isElevated(ctx):
    return ctx.author.id == MANAGER

### Commands ###
@bot.command(name="echo", help="echoes back to you!")
async def echo(ctx, message : str):
    await ctx.send(message)

@bot.command(name="update")
async def update(ctx):
    await ctx.send("Updating channel database.")
    con = sqlite3.connect(db.name(ctx))
    cur = con.cursor()
    db.update(ctx, con, cur)
    con.close()

@bot.command(name="delete_database")
@commands.check(isElevated)
async def delete_database(ctx):
    await ctx.send("Deleting channel database. Run rebuild_database to regenerate.")
    ret = db.delete(db.name(ctx))
    await ctx.send(f"Operation {ret}.")
@delete_database.error
async def delete_database_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Deletion requires elevated permissions.')

@bot.command(name="rebuild_database")
@commands.check(isElevated)
async def rebuild_database(ctx):
    await ctx.send("Rebuilding channel database. This may take a while.")
    con = sqlite3.connect(db.name(ctx))
    cur = con.cursor()
    db.rebuild(ctx, con, cur)
    con.close()
    await ctx.send("Operation complete.")
@rebuild_database.error
async def rebuild_database_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Rebuild requires elevated permissions.')

bot.run(TOKEN)
