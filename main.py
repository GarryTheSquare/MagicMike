# This example requires the 'message_content' intent.

import discord
import json
import requests
import os

discordToken = os.getenv("DISCORD_TOKEN")


def getCard(searchString):
    try:
        url = "https://api.scryfall.com/cards/named?fuzzy=" + searchString
        obj = requests.get(url)
        JSONobj = json.loads(obj.content)
        return JSONobj['image_uris']['normal']
    except: 
        return "Could not find card for (" + searchString + ")"


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '[[' in message.content:
        cards = message.content.split('[[')
        del cards[0]
        header = "Results for: "
        out = ""
        print(cards)
        for c in cards:
            if not ']]' in c:
                print("Error, invalid string")
                return
            c = c.split(']]')[0]
            header += c + ", "
            await message.channel.send(getCard(c))

    if message.content.startswith('!card '):
        cardString = message.content[6:]
        await message.channel.send(getCard(cardString))

client.run(discordToken)