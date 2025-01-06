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


@client.command()
@channel("make-channel")
async def make(ctx):
    try:
        words = ctx.message.content.split()

        if len(words) != 2:
            await ctx.send("Invalid format! Use: `~make <channel-name>`")
            return

        channel_name = words[1]
        current_category = ctx.channel.category

        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if existing_channel:
            await ctx.send(f"A channel with the name '{channel_name}' already exists.")
            return

        new_text = await ctx.guild.create_text_channel(name=channel_name, category=current_category)
        new_voice = await ctx.guild.create_voice_channel(name=channel_name, category=current_category)

        overwrite = new_text.overwrites_for(ctx.message.author)
        overwrite.read_messages = True
        overwrite.attach_files = True
        overwrite.send_voice_messages = True
        overwrite.create_polls = True
        overwrite.manage_messages = True
        overwrite.connect = True  
        overwrite.stream = True
        overwrite.speak = True 
        overwrite.send_messages = True
        await new_text.set_permissions(ctx.message.author, overwrite=overwrite)

        await new_voice.set_permissions(ctx.message.author, overwrite=overwrite)

        await new_text.send("To add someone to this channel, use: ~add @user. This will add them to both the VC channel and this Text channel!")
        await new_text.send("To remove someone then you do ~remove @user.")
        await new_text.send("If you want to delete the channel then do ~delete!")
        await new_text.send("Note: Only the maker of the channel has access to Pin, and delete messages!!!")
        await ctx.send(f"Channel '{channel_name}' created successfully!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command()
async def remove(ctx, user: discord.Member):
    try:
        # Check if the command is being used in a server text channel
        if not ctx.channel:
            await ctx.send("This command can only be used in a server text channel.")
            return

        # Get the text channel (the current channel where the command is run)
        text_channel = ctx.channel

        # Find the matching voice channel by name
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=text_channel.name)

        # Remove user from the text channel
        overwrite = text_channel.overwrites_for(user)
        if overwrite.read_messages is not None:  # Check if the user has specific permissions set
            await text_channel.set_permissions(user, overwrite=None)
            await ctx.send(f"{user.mention} has been removed from the text channel '{text_channel.name}'.")
        else:
            await ctx.send(f"{user.mention} does not have access to the text channel '{text_channel.name}'.")

        # Remove user from the voice channel if it exists
        if voice_channel:
            overwrite = voice_channel.overwrites_for(user)
            if overwrite.view_channel is not None:  # Check if the user has specific permissions set
                await voice_channel.set_permissions(user, overwrite=None)
                await ctx.send(f"{user.mention} has been removed from the voice channel '{voice_channel.name}'.")
            else:
                await ctx.send(f"{user.mention} does not have access to the voice channel '{voice_channel.name}'.")
        else:
            await ctx.send("No matching voice channel found.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



@client.command()
async def delete(ctx):
    try:
        # Check if the command is being used in a server text channel
        if not ctx.channel:
            await ctx.send("This command can only be used in a server text channel.")
            return

        if(ctx.channel.id == 1325657790760357898):
            await ctx.send("Guys laugh at this guy, he tried to delete this channel")
            emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
            await ctx.message.add_reaction(emoji)
            return

        # Check if the text channel is under the "Private Channels" category
        category_name = "Private Channels"
        if ctx.channel.category and ctx.channel.category.name != category_name:
            await ctx.send(f"This command can only be used in channels under the '{category_name}' category.")
            return

        # Get the text channel (the current channel where the command is run)
        text_channel = ctx.channel

        # Find the matching voice channel by name BEFORE deleting the text channel
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=text_channel.name)

        # Delete the voice channel if it exists
        if voice_channel:
            await voice_channel.delete()
            await ctx.send(f"Voice channel '{voice_channel.name}' deleted.")
        else:
            await ctx.send("No matching voice channel found.")

        # Delete the text channel
        await text_channel.delete()
        await ctx.send(f"Text channel '{text_channel.name}' deleted.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



@client.command()
async def add(ctx, user: discord.Member):
    try:
        if not ctx.channel:
            await ctx.send("This command can only be used in a server text channel.")
            return

        text = ctx.channel
        if text.overwrites_for(user).read_messages:
            await ctx.send(f"{user.mention} already has access to this channel.")
            return

        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.channel.name)
        if not voice_channel:
            await ctx.send("No matching voice channel found.")
            return

        overwrite = text.overwrites_for(ctx.message.author)
        overwrite.read_messages = True
        overwrite.attach_files = True
        overwrite.send_voice_messages = True
        overwrite.create_polls = True
        overwrite.connect = True  
        overwrite.stream = True
        overwrite.speak = True 
        overwrite.send_messages = True 
        await text.set_permissions(user, overwrite=overwrite)

        await voice_channel.set_permissions(user, overwrite=overwrite)

        await ctx.send(f"{user.mention} has been added to the channel!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


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
    dmChannel = client.get_channel(1325646285130301470)
    await dmChannel.send(f"{message.author} said: {message.content}")
    await dmChannel.send(f"{message.author.id} {message.author}")


# Logging events
async def LogEvent(user, message):
    logs_channel = client.get_channel(1307031962057183282)
    await logs_channel.send(f"<@{user.id}>: {message}")

client.run("MTIxMzYwNjM5NzQwMTYzNjg3NA.GX3LVs.GoPVFfD_4U6cMQ7Yk0dM16vV08GtrFeIcmAAQs")