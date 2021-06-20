#!/usr/bin/env python
"""
Discord bot for counting chat analysis. WIP.
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
#import numpy as np
#import matplotlib.pyplot as plt

import manageDB as db
import extract

### Get environment variables ###
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")
MANAGER = os.getenv("MANAGER_ID")

### Bot client and database initialization ###
bot = commands.Bot(command_prefix=PREFIX)

### Checks ###
async def isElevated(ctx):
    return ctx.author.id == MANAGER

### Commands ###
@bot.command(name="echo", help="echoes back to you!")
async def echo(ctx, message : str):
    await ctx.send(message)

@bot.command(name="rebuild_database")
@commands.check(isElevated)
async def rebuild_database(ctx):
    await ctx.send("Rebuilding channel database. This may take a while.")
    con = sqlite3.connect(f"database/{ctx.guild}{ctx.channel}.db")
    cur = con.cursor()
    db.rebuild(con, cur)
@rebuild_database.error
async def rebuild_database_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Require elevated permissions.')

bot.run(TOKEN)
