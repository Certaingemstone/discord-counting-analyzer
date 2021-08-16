#!/usr/bin/env python
"""
Discord bot for counting chat analysis. WIP.
"""

import os
from os import getenv
import io
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

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
@bot.command(name="count", help="The total number of messages in the counting channel")
@commands.check(isBound)
async def count(ctx):
    # update data
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur)
    # get data
    cur.execute("SELECT COUNT(*) FROM messages")
    count = cur.fetchone()[0]
    cur.execute("SELECT * FROM messages ORDER BY created_timestamp DESC LIMIT 1")
    last = cur.fetchone()
    number = last[-1]
    await ctx.send(f"We should be on {count}, and I'm reading {number}.")
@count.error
async def count_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Need to be bound to a channel.")


@bot.command(name="history", help="Error in messages in the counting channel over last N")
@commands.check(isBound)
async def history(ctx, N):
    # update data
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur)
    # get data
    cur.execute("SELECT * FROM messages ORDER BY created_timestamp ASC")
    errors = []
    for count, row in enumerate(cur):
        delta = row[-1] - count # actual number - number it's supposed to be
        errors.append(delta)
    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) # rows, columns, index
    ax.set_title("error vs. message")
    ax.set_xlabel("message")
    ax.set_ylabel("error")
    ax.plot(errors, color='blue', marker='o', linestyle='dashed', lw=2, markersize=5)
    # Export
    buffer = io.BytesIO()
    fig.savefig(buffer, format='jpg')
    buffer.seek(0)
    imageFile = discord.File(fp=buffer, filename="graph.jpg")
    await ctx.send(file=imageFile)
@history.error
async def history_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Need to be bound to a channel.")


@bot.command(name="leaderboard", help="Top counters in the last N counts; if no N given, reads the entire channel. If not specified, finds top 3.")
@commands.check(isBound)
async def leaderboard(ctx, top=3, N=0):
    # get how many messages to look back
    if not N == 0:
        try:
            N = int(N)
            if N < 0:
                N = -N
        except:
            await ctx.send("Oops! I couldn't interpret that as a number!")
    # update data
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur, overlap=10)
    # get data
    if not N == 0:
        cur.execute(f"SELECT * FROM messages ORDER BY created_timestamp DESC LIMIT {N}")
        title = "Leaderboard"
        description = f"Stats taken over the last {N} messages"
    else:
        cur.execute(f"SELECT * FROM messages ORDER BY created_timestamp DESC")
        title = "Leaderboard"
        description = f"Stats taken over all messages"
    counters = dict()
    editors = dict()
    # analyze the data
    for row in cur:
        # message count
        author = row[1]
        if author in counters:
            counters[author] = counters[author] + 1
        else:
            counters[author] = 1
        # edit count
        edited_timestamp = row[3]
        if not edited_timestamp == -1:
            if author in editors:
                editors[author] = editors[author] + 1
            else:
                editors[author] = 1
    # build the leaderboard
    author_counts = []
    editor_counts = []
    for author in counters:
        author_counts.append((author, counters[author])) # (author, # of messages)
    for author in editors:
        editor_counts.append((author, editors[author]))
    author_counts.sort(key = lambda x: x[1], reverse=True) # sort by # of messages sent
    editor_counts.sort(key = lambda x: x[1], reverse=True)
    # construct the message
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green())
    i = 0
    for tup in author_counts:
        if i == top:
            break
        embed.add_field(name=tup[0], value=f"{tup[1]} counts", inline=True)
        i += 1
    embed.add_field(name="*Most edits:*", value=f"{editor_counts[0][0]} with {editor_counts[0][1]} edits", inline=False)
    await ctx.send(embed=embed)
@leaderboard.error
async def leaderboard_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Need to be bound to a channel.")

### Management Commands ###
@bot.command(name="update")
async def update(ctx):
    await ctx.send("Updating channel database.")
    con = sqlite3.connect(db.databaseName(ctx))
    cur = con.cursor()
    await db.update(ctx, con, cur)
    await ctx.send("Success.")
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
    cur.execute("DROP TABLE messages")
    targetChannel = await db.rebuild(ctx, con, cur)
    con.close()
    await ctx.send(f"Operation success on {targetChannel}.")
@rebuild.error
async def rebuild_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Rebuild requires elevated permissions.')

bot.run(TOKEN)
