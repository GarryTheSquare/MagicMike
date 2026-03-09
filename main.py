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
        for s in cardString.split(';'):
            await message.channel.send(getCard(s))
    
    if message.content == "!help":
        out =   "Hi, I turn magic card names into images of those cards. If you would like me to post a picture of cards, you can:\n"
        out +=  "`!card island` (for 1 card)\n"
        out +=  "!card island;mountain;swamp` (for multiple cards)\n"
        out +=  "Or in any message, put brackets around the cardname like `I think of adding [[island]] or [[mountain]] to my deck`\n"
        out +=  "\n"
        out +=  "I try to correct typos as well as I can. If you want technical/programming info about how I work, type !about-me"
        await message.channel.send(out)

    if message.content == "!about-me":
        out +=	"I run on a Python library for Discord bots! I take your card names and run them through the Scryfall REST API to get all the info about the card, and then post the URL of that image to the discord server. Discord then displays that URL as an image!\n"
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