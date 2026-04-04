# This example requires the 'message_content' intent.

import discord
import json
import requests
import os
import re

discordToken = os.getenv("DISCORD_TOKEN")

def getCard(searchString):
    try:
        cardSet, searchString = getSet(searchString)
        if cardSet != None:
            try:
                url = "https://api.scryfall.com/cards/named?fuzzy=" + searchString + "&set=" + cardSet
                print(url)
                obj = requests.get(url)
                JSONobj = json.loads(obj.content)
                return JSONobj['image_uris']['normal'], banChecK(JSONobj['legalities'])
            except:
                return "Could not find this card for set " + cardSet + ". Trying again without specifying the set\n" + getCard(searchString)
        url = "https://api.scryfall.com/cards/named?fuzzy=" + searchString
        obj = requests.get(url)
        JSONobj = json.loads(obj.content)
        return JSONobj['image_uris']['normal'], banChecK(JSONobj['legalities'])
    except: 
        return "Could not find card for (" + searchString + ")"
    
def banChecK(card):
    out = ""
    if (card['commander'] !="legal"):
        out += "Legality for commander: " + card['commander'] + '\n'
    if (card['standard'] !="legal"):
        out += "Legality for standard: " + card['commander'] + '\n'
    return out

def getSet(s):
    match = re.search(r'\(([A-Za-z0-9]{3})\)', s)
    
    if match:
        code = match.group(1)
        cleaned = s[:match.start()] + s[match.end():]
        return code, cleaned
    
    return None, s


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
            card, legalMsg = getCard(c)
            if (len(legalMsg) > 0):
                await message.channel.send(legalMsg)
            await message.channel.send(card)

    if message.content.startswith('!card '):
        cardString = message.content[6:]
        for s in cardString.split(';'):
            card, legalMsg = getCard(c)
            if (len(legalMsg) > 0):
                await message.channel.send(legalMsg)
            await message.channel.send(card)
    
    if message.content == "!help mtg":
        out =   """Hi, I turn magic card names into images of those cards. If you would like me to post a picture of cards, you can:\n
        `!card island` (for 1 card)\n
        `!card island;mountain;swamp` (for multiple cards)\n
        `!card island (TLA)` You can also specify a specific printing by adding the set code inbetween brackets anywhere in the command.
        Or in any message, put brackets around the cardname like `I think of adding [[island]] or [[mountain]] to my deck`\n
        \n
        I try to correct typos as well as I can. If you want technical/programming info about how I work, type !about-me"""
        await message.channel.send(out)

    if message.content == "!about-me mtg":
        out =	"I run on a Python library for Discord bots! I take your card names and run them through the Scryfall REST API to get all the info about the card, and then post the URL of that image to the discord server. Discord then displays that URL as an image!\n"
        out +=	"\n"
        out +=	"I am hosted on a Cloud Computing Service called Railway that comes with a nice free tier of service hosting for small scripts like me. Hosting me costs about 1,6 cents per day, and this service does not bill you for the first euro per month.\n"
        out +=	"\n"
        out +=	"Here is the link to my GitHub Repo and the mentioned resources:\n"
        out +=	"\n"
        out +=	"`GitHub Repo: (https://github.com/GarryTheSquare/MagicMike)\n"
        out +=	"Discord.py (https://discordpy.readthedocs.io/en/stable/)\n"
        out +=	"Scryfall REST API (https://scryfall.com/docs/api)\n"
        out +=	"Railway Cloud Service (https://railway.com/)`"
        await message.channel.send(out)

client.run(discordToken)