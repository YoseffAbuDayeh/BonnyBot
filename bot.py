import asyncio
import discord  # type: ignore
from discord.ext import commands as command
import random
import os
from dotenv import load_dotenv
from methods import method
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
    Listener that will trigger on each message sent

    param:
    message: the message, this contains information all from the contents inside the message to the type of message.
    '''

    if message.author == client.user:
        return

    if message.author.id == 975013661452140554:
        await method.LogEvent(message.author, client, "Deleting Ryan's message: " + message.content)
        await message.delete()
        return

    if random.random() < 0.3:
        emojis = [
            discord.PartialEmoji(name="ThisTBH", id=1266540721377247272),
            discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248),
            discord.PartialEmoji(name="vycerage128", id=1227633746111365201),
            discord.PartialEmoji(name="octaviaderp", id=1227633669351411816),
            discord.PartialEmoji(name="BonnyCry", id=1420996430843347084),
        ]

        default_emoji = discord.PartialEmoji(name="BonnyPeek", id=1420997790791761932)

        chosen = random.choice(emojis + [default_emoji])
        await message.add_reaction(chosen)



    await client.process_commands(message)


async def main():
    load_dotenv()
    await client.load_extension("methods.commands")
    await client.load_extension("methods.ai")
    await client.load_extension("ssb.stream")
    discord_token = os.getenv("TOKEN")
    await client.start(discord_token)


if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())
