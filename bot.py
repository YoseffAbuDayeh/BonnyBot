import discord # type: ignore
from discord.utils import get
from discord.ext import commands
import random
import asyncio


intents = discord.Intents.all()
client = commands.Bot(command_prefix="~", intents=intents)
#Permission number: 50564110462193 idk where to put it though


def channel(channel_name):
  def predicate(ctx):
    return ctx.channel.name == channel_name
  return commands.check(predicate)




def notChannel(channel_name):
  def predicate(ctx):
    return ctx.channel.name != channel_name
  return commands.check(predicate)







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
  if (random.random() * 1000) < 3:
    emoji = discord.PartialEmoji(name="ThisTBH", id=1266540721377247272)
    await message.add_reaction(emoji)

  if message.author == client.user:
    return



  

  if message.author.name == "shas7459":
    await message.channel.purge(limit=2, check=lambda msg: not msg.pinned)

  await client.process_commands(message)



@client.event
@notChannel("general")
async def on_message(message):
  try:
      emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
      await message.add_reaction(emoji)
  except:
    emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
    await message.add_reaction(emoji) #This means that it is not a channel rather a DM
    await DMsTexts(message)

  await client.process_commands(message)



@client.command()
async def yo(ctx): #To change!!!
    test = await client.fetch_user(631460227132162068)
    await test.send(ctx.message.content)



@client.command()
@channel("irl-commands")
async def role(ctx):
  try:
    words = ctx.message.content.split()

    if len(words) != 3:
      await ctx.send("Invalid format! Use: `@user role_name`")
      return

    user_mention = words[1]
    role_name = words[2]

    member = discord.utils.get(ctx.guild.members, mention=user_mention)
    if not member:
      await ctx.send("User not found in this server!")
      return

    role = get(ctx.guild.roles, name=role_name)
    if not role:
      await ctx.send(f"Role {role_name} not found!")
      return
    
    await member.add_roles(role)
    await ctx.send(f"Added role {role.name} to {member.mention} ({member}).")
    LogEvent(ctx.author, f"Gave the role {role_name} to {member}")


  except Exception as e:
    await ctx.send(f"An error occurred: {e}")

@client.command()
@channel("irl-commands")
async def unrole(ctx):
  try:
    words = ctx.message.content.split()

    if len(words) != 3:
      await ctx.send("Invalid format! Use: `@user role_name`")
      return

    user_mention = words[1]
    role_name = words[2]

    member = discord.utils.get(ctx.guild.members, mention=user_mention)
    if not member:
      await ctx.send("User not found in this server!")
      return

    role = get(ctx.guild.roles, name=role_name)
    if not role:
      await ctx.send(f"Role {role_name} not found!")
      return

    await member.remove_roles(role)
    await ctx.send(f"Removed role {role.name} to {member.mention} ({member}).")
    LogEvent(ctx.author, f"Removed the role {role_name} from {member}")

  except Exception as e:
    await ctx.send(f"An error occurred: {e}")


@client.command()
async def clear(ctx):
  await ctx.channel.purge(limit=1000, check=lambda msg: not msg.pinned)
  logs_channel = client.get_channel(1307031962057183282)
  if logs_channel:
      await logs_channel.send(f"<@{ctx.author.id}> ({ctx.author}) cleared the channel <#{ctx.channel.id}>.")



async def DMsTexts(message): 
  dmChannel = client.get_channel(1316239219131420672)
  await dmChannel.send(f"{message.author} said: {message.content}")
  await dmChannel.send(f"{message.author.id} {message.author}")




#To do: Incorporate the Logging of the deleting messages to this/make a overloading/dispatch for this.
async def LogEvent(user, message):
  logs_channel = client.get_channel(1307031962057183282);  
  logs_channel.send(f"{user}: {message}")



client.run("MTIxMzYwNjM5NzQwMTYzNjg3NA.GX3LVs.GoPVFfD_4U6cMQ7Yk0dM16vV08GtrFeIcmAAQs")
