#!/usr/bin/env python
"""
Discord bot for counting chat analysis. WIP.
"""

import os

import discord
from dotenv import load_dotenv
#import numpy as np
#import matplotlib.pyplot as plt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
