#!/usr/bin/env python
"""
Discord bot for counting chat analysis. WIP.
"""

import os
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

async def isBound(ctx):
    nameFile = f"database/{ctx.guild}.txt"
    return os.path.exists(nameFile)

### User Commands ###
@bot.command(name="count", help="the total number of messages in the counting channel")
@commands.check(isBound)
async def count(ctx):
    # update data
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur)
    # get data
    cur.execute("SELECT COUNT(*) FROM messages")
    count = cur.fetchone()[0]
    cur.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 1")
    last = cur.fetchone()
    content = last[4]
    number = extract.findNumber(content)
    await ctx.send(f"We should be on {count}, and I'm reading {number}.")
@count.error
async def count_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Need to be bound to a channel.")

### Management Commands ###
@bot.command(name="update")
async def update(ctx):
    await ctx.send("Updating channel database.")
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur)
    con.close()

@bot.command(name="delete")
@commands.check(isElevated)
async def delete(ctx):
    await ctx.send("Deleting database.")
    ret = db.delete(db.databaseName(ctx))
    await ctx.send(f"Operation {ret}.")
@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Deletion requires elevated permissions.')

@bot.command(name="bind")
@commands.check(isElevated)
async def bind(ctx, channelName : str):
    nameFile = f"database/{ctx.guild}.txt"
    channel = discord.utils.get(ctx.guild.channels, name=channelName)
    if channel is not None:
        ID = channel.id
        with open(nameFile, "w") as file:
            file.write(str(ID))
        await ctx.send(f"Bound to channel {channelName} with ID {ID}.")
    else:
        await ctx.send(f"Couldn't find channel {channelName}.")

@bot.command(name="rebuild")
@commands.check(isElevated)
async def rebuild(ctx):
    await ctx.send("Acknowledge.")
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    targetChannel = await db.rebuild(ctx, con, cur)
    con.close()
    await ctx.send(f"Operation success on {targetChannel}.")
@rebuild.error
async def rebuild_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Rebuild requires elevated permissions.')

bot.run(TOKEN)
