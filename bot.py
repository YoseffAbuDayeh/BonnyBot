import asyncio
import discord  # type: ignore
from discord.ext import commands as command
import random
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
client = command.Bot(command_prefix="~", intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# General on-message event
@client.event
async def on_message(message):
    '''
    Listener that will triggered on each message sent

    param:
    message: the message, this contains information all from the contents inside the message to the type of message.
    '''
    if random.random() < 0.1:
        emoji = discord.PartialEmoji(name="ThisTBH", id=1266540721377247272)
        await message.add_reaction(emoji)  # Funny emote
    if random.random() < 0.2:
        emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
        await message.add_reaction(emoji)

    if message.author == client.user:
        return

    await client.process_commands(message)


async def main():
    load_dotenv()
    await client.load_extension("methods.commands")
    await client.load_extension("methods.ai")
    discord_token = os.getenv("TOKEN")
    await client.start(discord_token)

if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())
