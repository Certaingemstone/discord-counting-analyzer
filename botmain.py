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
MANAGER = int(getenv("MANAGER_ID"))

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

@bot.command(name="delete")
@commands.check(isElevated)
async def delete(ctx):
    await ctx.send("Deleting channel database.")
    ret = db.delete(db.name(ctx))
    await ctx.send(f"Operation {ret}.")
@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Deletion requires elevated permissions.')

@bot.command(name="rebuild")
@commands.check(isElevated)
async def rebuild(ctx):
    await ctx.send("Rebuilding channel database. This may take a while.")
    con = sqlite3.connect(db.name(ctx))
    print("connected")
    cur = con.cursor()
    print("made cursor")
    await db.rebuild(ctx, con, cur)
    print("ran function")
    con.commit()
    print("committed")
    con.close()
    await ctx.send("Operation success.")
@rebuild.error
async def rebuild_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Rebuild requires elevated permissions.')

bot.run(TOKEN)
