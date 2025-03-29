from discord.ext import commands

class Helpers(commands.Cog):
    bot = None
    def __init__ (self, bot):
        Helpers.bot = bot
    
    @classmethod
    def getBot(cls):
        return cls.bot
    
    @classmethod
    def setBot(cls, Bot):
        cls.bot = Bot


    
def getBot():
    return Helpers.GetBot()

def setup(bot):
    bot.add_cog(Helpers(bot))