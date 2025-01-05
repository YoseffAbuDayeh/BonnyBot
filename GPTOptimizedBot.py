import discord  # type: ignore
from discord.utils import get
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix="~", intents=intents)


# Decorators for channel checking
def channel(channel_name):
    async def predicate(ctx):
        return ctx.guild and ctx.channel.name == channel_name
    return commands.check(predicate)


# Bot ready event
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# Merge on_message events
@client.event
async def on_message(message):
    if (random.random() * 1000) < 3:
        emoji = discord.PartialEmoji(name="ThisTBH", id=1266540721377247272)
        await message.add_reaction(emoji)

    if message.author == client.user:
        return

    if message.author.name == "shas7459":
        await message.channel.purge(limit=2, check=lambda msg: not msg.pinned)

    # Handle DMs
    if not message.guild:
        emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
        await message.add_reaction(emoji)
        await DMsTexts(message)

    await client.process_commands(message)


# Command to add roles
@client.command()
async def role(ctx):
    try:
        words = ctx.message.content.split()
        if len(words) != 3:
            await ctx.send("Invalid format! Use: `@user role_name`")
            return

        user_mention, role_name = words[1], words[2]
        member = discord.utils.get(ctx.guild.members, mention=user_mention)
        if not member:
            await ctx.send("User not found in this server!")
            return

        # Restrict roles
        if role_name in ["Mod", "Bot"]:
            await ctx.send(f"I can't assign the role '{role_name}'.")
            return

        role = get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Role {role_name} not found!")
            return

        # Check channel and assign
        if ctx.channel.name == "bot":
            await member.add_roles(role)
            await ctx.send(f"Added role {role.name} to {member.mention}.")
        elif ctx.channel.name == "irl-commands":
            await member.add_roles(role)
            await ctx.send(f"Added role {role.name} to {member.mention}.")
        else:
            await ctx.send("This command is not allowed in this channel.")

        await LogEvent(ctx.author, f"Gave the role {role_name} to {member}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Command to remove roles
@client.command()
async def unrole(ctx):
    try:
        words = ctx.message.content.split()
        if len(words) != 3:
            await ctx.send("Invalid format! Use: `@user role_name`")
            return

        user_mention, role_name = words[1], words[2]
        member = discord.utils.get(ctx.guild.members, mention=user_mention)
        if not member:
            await ctx.send("User not found in this server!")
            return

        # Restrict roles
        if role_name in ["Mod", "Bot"]:
            await ctx.send(f"I can't remove the role '{role_name}'.")
            return

        role = get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Role {role_name} not found!")
            return

        # Check channel and remove
        if ctx.channel.name == "bot":
            await member.remove_roles(role)
            await ctx.send(f"Removed role {role.name} from {member.mention}.")
        elif ctx.channel.name == "irl-commands":
            await member.remove_roles(role)
            await ctx.send(f"Removed role {role.name} from {member.mention}.")
        else:
            await ctx.send("This command is not allowed in this channel.")

        await LogEvent(ctx.author, f"Removed the role {role_name} from {member}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Command to clear messages
@client.command()
async def clear(ctx):
    await ctx.channel.purge(limit=1000, check=lambda msg: not msg.pinned)
    logs_channel = client.get_channel(1307031962057183282)
    if logs_channel:
        await logs_channel.send(f"<@{ctx.author.id}> cleared the channel <#{ctx.channel.id}>.")


# Utility function to handle DMs
async def DMsTexts(message):
    dmChannel = client.get_channel(1316239219131420672)
    await dmChannel.send(f"{message.author} said: {message.content}")
    await dmChannel.send(f"{message.author.id} {message.author}")


# Logging events
async def LogEvent(user, message):
    logs_channel = client.get_channel(1307031962057183282)
    await logs_channel.send(f"<@{user.id}>: {message}")

client.run("MTIxMzYwNjM5NzQwMTYzNjg3NA.GX3LVs.GoPVFfD_4U6cMQ7Yk0dM16vV08GtrFeIcmAAQs")