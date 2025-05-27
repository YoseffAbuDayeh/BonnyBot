import asyncio
import discord  # type: ignore
from discord.ext import commands as command
import random
import os
from dotenv import load_dotenv
import cohere
from collections import deque
from methods import commands
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

    if random.random() < 0.2:
        chat_history = deque(maxlen=2)
        chat_history.append({"role": "USER", "message": message.content})
        response = client.cohere.chat(
            message=message.content,
            model="command-r-plus",
            chat_history=[],
            temperature=0.2,
            preamble="You are \"Bonny\" a, shy, and silly member."
                     "If you don't have anything to add to the conversation, just ask regarding something."
                     "You like to say silly things, and sometimes misunderstand you start rambling."
                     "You never take things too seriously. Keep responses short and lighthearted!"
        )  # TODO: Fix Bonny's context. I feel if she has a backstory then it would help the responses be more accurate to her character

        await message.channel.send(response.text.strip())

    await client.process_commands(message)


async def main():
    load_dotenv()
    cohere_key = os.getenv("KEY")
    co = cohere.Client(cohere_key)
    client.cohere = co
    await client.load_extension("methods.commands")
    discord_token = os.getenv("TOKEN")
    await client.start(discord_token)

if __name__ == '__main__':
    asyncio.run(main())