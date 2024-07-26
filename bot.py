import discord # type: ignore
import os
import random


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
client = discord.Client(intents=intents)
#Permission number: 50564110462193 idk where to put it though

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")

@client.event
async def on_message_delete(message):
  if message.author == client.user:
    return
  await message.channel.send(f"I saw what you did there, <@{message.author.id}> <:FiniiOgey:1227633857382322248>")



@client.event
async def on_message(message):
  if message.author == client.user:
      return
  if message.author.name == "shas7459" or message.author.name == "shawnywrestling":
    await message.channel.purge(limit=1, check=lambda msg: not msg.pinned)
  
  if(message.channel.name != "general" and message.channel.name != "roles" and message.channel.name != "roles-without-ping"):
    await message.add_reaction("<:FiniiOgey:1227633857382322248>")
  
  
  if(message.content == "!clear"):
    await message.channel.purge(limit=1000, check=lambda msg: not msg.pinned)

  # await message.channel.send(f"Message Content: {message.content}")
  

client.run("MTIxMzYwNjM5NzQwMTYzNjg3NA.GX3LVs.GoPVFfD_4U6cMQ7Yk0dM16vV08GtrFeIcmAAQs")