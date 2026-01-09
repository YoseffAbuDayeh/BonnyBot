import discord
from discord.ext import commands
from dotenv import load_dotenv


class ChatCommands(commands.Cog):
    def __init__(self):
        crewbattles = {}
        '''
        The Crew battle is a dictionary of string (channel ID) : CB (object)
        '''

#TODO everything, I forgot what I was doing here tbh.


    @commands.command()
    async def start(self, ctx, TeamA: str, TeamB:str, Size: int):
        '''
        This method will start a crew battle.

        :param message: The current message It also uses a chat history.
         '''

        if TeamA == None or TeamB == None:
            return await ctx.send("Please specify both a Team A and a Team B.")
        if Size == None:
            return await ctx.send("Please specify the size of the crew battle.")





        # embed = discord.Embed(
        #     title="Crew Battle Started",
        #     description="Team Red vs Team Blue",
        #     color= 0xFF5C00
        # )
        #
        # embed.add_field(
        #     name="🟥 Team Red",
        #     value="• ChatGPT\n• RoboPilot\n• MegaMind",
        #     inline=True
        # )
        #
        # embed.add_field(
        #     name="🟦 Team Blue",
        #     value="• ClaudeAI\n• GeminiPro\n• FalconBrain",
        #     inline=True
        # )
        # embed.add_field(
        #     name="🟦 Team Blue",
        #     value="• ClaudeAI\n• GeminiPro\n• FalconBrain",
        #     inline=False
        # )
        #
        # embed.set_footer(text="Round 1 — Waiting for starters...")
        # # await message.channel.send(embed=embed)


# Setup function for
# bot.load_extension("methods.ai")
async def setup(bot):
    load_dotenv()
    await bot.add_cog(ChatCommands())
