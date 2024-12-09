import discord # type: ignore
from discord.utils import get
from discord.ext import commands
import random


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
client = commands.Bot(command_prefix="~", intents=intents)
#Permission number: 50564110462193 idk where to put it though

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")

@client.event
async def on_message_delete(message):
  if message.author == client.user:
    return
  
  logs_channel = client.get_channel(1307031962057183282);  
  await logs_channel.send(f"<@{message.author.id}> ({message.author}) sent: {message.content}")
  for attachment in message.attachments:
    await logs_channel.send(attachment.url)
  await message.channel.send(f"I saw what you did there, <@{message.author.id}> <:FiniiOgey:1227633857382322248>")


@client.event
async def on_message(message):
    if (random.random() * 100) < 3:
        emoji = discord.PartialEmoji(name="ThisTBH", id=1266540721377247272)
        await message.add_reaction(emoji)

    if message.author == client.user:
        return

    if message.author.name == "shas7459":
        await message.channel.purge(limit=1, check=lambda msg: not msg.pinned)

    if message.channel.name != "general":
        emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
        await message.add_reaction(emoji)
  

    await client.process_commands(message)

@client.command() #This is not working, dunno why tbh
async def role(ctx):
  if ctx.channel.name == "irl-commands":
    try:
      words = ctx.message.content.split()

      if len(words) != 3:
        await ctx.send("Invalid format! Use: `@user role_name`")
        return

      # Extract the user mention and the role name
      user_mention = words[1]
      role_name = words[2]
      await ctx.send("```" + user_mention + "```")

      # Get the member (user) from the mention
      member = discord.utils.get(ctx.guild.members, mention=user_mention)
      await ctx.send(member)
      if not member:
        await ctx.send("User not found in this server!")
        return

      # Get the role by name
      role = get(ctx.guild.roles, name=role_name)
      if not role:
        await ctx.send(f"Role {role_name} not found!")
        return

      # Add the role to the member
      await member.add_roles(role)
      await ctx.send(f"Added role {role.name} to {member.mention}.")

    except Exception as e:
      await ctx.send(f"An error occurred: {e}")


@client.command()
async def clear(ctx):
  await ctx.channel.purge(limit=1000, check=lambda msg: not msg.pinned)
  logs_channel = client.get_channel(1307031962057183282)
  if logs_channel:
      await logs_channel.send(f"<@{ctx.author.id}> ({ctx.author}) cleared the channel.")


client.run("MTIxMzYwNjM5NzQwMTYzNjg3NA.GX3LVs.GoPVFfD_4U6cMQ7Yk0dM16vV08GtrFeIcmAAQs")