from discord.ext import commands
from util import decorators
import discord  # type: ignore
from discord.utils import get
from methods.method import LogEvent

class Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot         

    @commands.command()
    async def clear(self, ctx):
        """
        This command is going to clear the messages of a channel.

        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        """
        await ctx.channel.purge(limit=1000, check=lambda msg: not msg.pinned)

        await LogEvent(ctx.author,self.bot,  f"cleared the channel <#{ctx.channel.id}>.")

    @commands.command()
    @decorators.channel("make-channel")
    async def make(self, ctx):
        """
        This command makes a channel in the same category the message was sent.

        params:
        ctx: This has all the data of the message. From the message itself to where it was sent
        """
        try:
            words = ctx.message.content.split()

            #Error handling to make sure that the data is going to be properly processed
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
            #overwrite has both the voice channel and text channel data since it was giving me an issue having different overwrites.
            await new_text.set_permissions(ctx.message.author, overwrite=overwrite)

            await new_voice.set_permissions(ctx.message.author, overwrite=overwrite)

            await new_text.send("To add someone to this channel, use: ~add @user. This will add them to both the VC channel and this Text channel!")
            await new_text.send("To remove someone then you do ~remove @user.")
            await new_text.send("If you want to delete the channel then do ~delete!")
            await new_text.send("Note: Only the maker of the channel has access to Pin, and delete messages!!!")
            await ctx.send(f"Channel '{channel_name}' created successfully!")
            await LogEvent(ctx.author, self.bot, f"Made a channel: {channel_name}")
        except Exception as e:
            await ctx.send(f"So something happened... Ask a mod for help :)") #BREAKING OUT OF CHARACTER IS UNACCEPTABLE!!!
            await LogEvent(ctx.author, self.bot,f"An error occurred on channel <#{ctx.channel.id}>, the user did \"{ctx.message.content}\". Information about the error: {e}")

    @commands.command()
    async def remove(self, ctx, user: discord.Member):
        """
        This function will remove a user from the channel. Only available to the private channels!

        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        user: This has the data of the user to be removed from the channel
        """
        try:
            
            if ctx.channel.category.name != "Private Channels":
                await ctx.send("This command cannot be used outside of the private channels category.")
                return

            if ctx.channel.name == "make-channel":
                await ctx.send("I refuse.")
                return

            text_channel = ctx.channel

            # Find the matching voice channel by name
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=text_channel.name)

            # Remove user from the text channel if he has access
            overwrite = text_channel.overwrites_for(user)
            if overwrite.read_messages is not None: 
                await text_channel.set_permissions(user, overwrite=None)
                await ctx.send(f"{user.mention} has been removed from the text channel '{text_channel.name}'.")
            else:
                await ctx.send(f"{user.mention} does not have access to the text channel '{text_channel.name}'.")

            # Remove user from the voice channel if he has access
            if voice_channel:
                overwrite = voice_channel.overwrites_for(user)
                if overwrite.view_channel is not None: 
                    await voice_channel.set_permissions(user, overwrite=None)
                    await ctx.send(f"{user.mention} has been removed from the voice channel '{voice_channel.name}'.")
                else:
                    await ctx.send(f"{user.mention} does not have access to the voice channel '{voice_channel.name}'.")
            else:
                await ctx.send("No matching voice channel found.")

            await LogEvent(ctx.author, self.bot, f"Removed {user.name} from the {ctx.channel} channel.")
        except Exception as e:
            await ctx.send(f"So something happened... Ask a mod for help :)") 
            await LogEvent(ctx.author, self.bot, f"An error occurred on channel <#{ctx.channel.id}>, the user did \"{ctx.message.content}\". Information about the error: {e}")



    @commands.command()
    async def delete(self, ctx):
        """
        This function will delete the channel it is currently on.
        
        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        """
        try:
            if ctx.channel.category.name != "Private Channels":
                await ctx.send("This command cannot be used outside of the private channels category.")
                return

            #If they tried to delete the channel where one makes channels
            if(ctx.channel.id == 1325657790760357898): 
                await ctx.send("Guys laugh at this guy, he tried to delete this channel")
                emoji = discord.PartialEmoji(name="FiniiOgey", id=1227633857382322248)
                await ctx.message.add_reaction(emoji)
                return

            category_name = "Private Channels"
            if ctx.channel.category and ctx.channel.category.name != category_name:
                await ctx.send(f"This command can only be used in channels under the '{category_name}' category.")
                return

            text_channel = ctx.channel

            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=text_channel.name)

            if voice_channel:
                await voice_channel.delete()
                await ctx.send(f"Voice channel '{voice_channel.name}' deleted.")
            else:
                await ctx.send("No matching voice channel found.")

            await text_channel.delete()

            await LogEvent(ctx.author, self.bot, f"Deleted the channel {ctx.channel}")


    
        except Exception as e:
            await ctx.send(f"So something happened... Ask a mod for help :)") 
            await LogEvent(ctx.author, self.bot,  f"An error occurred on channel <#{ctx.channel.id}>, the user did \"{ctx.message.content}\". Information about the error: {e}")

    @commands.command()
    async def add(self, ctx, user: discord.Member):
        """
        Add someone to the text and voice channel with the same name.
        """
        try:
            if not isinstance(ctx.channel, discord.TextChannel):
                await ctx.send("This command can only be used in a server text channel.")
                return

            text = ctx.channel
            overwrite = text.overwrites_for(user)
            if overwrite.read_messages:
                await ctx.send(f"{user.mention} already has access to this channel.")
                return

            voice_channel = next(
                (ch for ch in ctx.guild.voice_channels if ch.name.lower() == ctx.channel.name.lower()),
                None
            )
            if not voice_channel:
                await ctx.send("No matching voice channel found.")
                return

            perm_overwrite = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                attach_files=True,
                speak=True,
                connect=True,
                stream=True,
                send_voice_messages=True,
                create_polls=True
            )

            await text.set_permissions(user, overwrite=perm_overwrite)
            await voice_channel.set_permissions(user, overwrite=perm_overwrite)

            await ctx.send(f"{user.mention} has been added to the channel!")
            await LogEvent(ctx.author, self.bot, f"Added {user} to the {ctx.channel} channel.")

        except Exception as e:
            print(e)
            await ctx.send(f"Something went wrong. Ask a mod for help :)")
            await LogEvent(ctx.author, self.bot,
                           f"An error occurred on channel <#{ctx.channel.id}>, user ran \"{ctx.message.content}\". Error: {e}")

    @commands.command()
    async def role(self, ctx):
        """
        This command will give a role to the user. User is supposed to say role, @ the user and then type the name of the role afterward
        
        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        """
        try:
            words = ctx.message.content.split()
            if len(words) != 3:
                await ctx.send("Invalid format! Use: `@user role_name`")
                return

            user_mention, role_name = words[1], words[2]
            #Gets the user from the mention if he is in the server
            member = discord.utils.get(ctx.guild.members, mention=user_mention)
            if not member:
                await ctx.send("User not found in this server!")
                return

            if role_name in ["Mod", "Bot"]:
                await ctx.send(f"I can't assign the role '{role_name}'.")
                return

            role = get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"Role {role_name} not found!")
                return


            if ctx.channel.name == "bot":
                await member.add_roles(role)
                await ctx.send(f"Added role {role.name} to {member.mention}.")
            elif ctx.channel.name == "irl-commands":
                await member.add_roles(role)
                await ctx.send(f"Added role {role.name} to {member.mention}.")
            else:
                await ctx.send("This command is not allowed in this channel.")

            await LogEvent(ctx.author, self.bot, f"Gave the role {role_name} to {member}")

        except Exception as e:
            await ctx.send(f"So something happened... Ask a mod for help :)") 
            await LogEvent(ctx.author, self.bot, f"An error occurred on channel <#{ctx.channel.id}>, the user did \"{ctx.message.content}\". Information about the error: {e}")


    @commands.command()
    async def unrole(self, ctx):
        """
        This command will take a role to the user. User is supposed to say un-role, @ the user and then type the name of the role afterward
        
        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        """
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

            if role_name in ["Mod", "Bot"]:
                await ctx.send(f"I can't remove the role '{role_name}'.")
                return

            role = get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"Role {role_name} not found!")
                return

            if ctx.channel.name == "bot":
                await member.remove_roles(role)
                await ctx.send(f"Added role {role.name} to {member.mention}.")
            elif ctx.channel.name == "irl-commands":
                await member.remove_roles(role)
                await ctx.send(f"Removed role {role.name} from {member.mention}.")
            else:
                await ctx.send("This command is not allowed in this channel.")

            await LogEvent(ctx.author, self.bot, f"Removed the role {role_name} from {member}")

        except Exception as e:
            await ctx.send(f"So something happened... Ask a mod for help :)") 
            await LogEvent(ctx.author, self.bot,f"An error occurred on channel <#{ctx.channel.id}>, the user did \"{ctx.message.content}\". Information about the error: {e}")





async def setup(bot):
    await bot.add_cog(Command(bot))