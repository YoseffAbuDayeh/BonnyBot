from util import helperMethods
from discord.utils import get

async def DMsTexts(message):
        '''
        This command is going to grab the message and put it on a specific channel. Used in-case someone DMs Bonny (the bot), which they shouldn't.

        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        '''
        
        dmChannel = get(helperMethods.getBot().channels, name="dms")
        await dmChannel.send(f"{message.author} ({message.author.id}) said: {message.content}")


    # Logging events
async def LogEvent(user, message):
    '''
    This method will log the events in the logs channel.

    params:
    user: This variable has all the data of the user.
    message: This variable has the message of the action performed.
    '''
    logsChannel = get(helperMethods.getBot().channels, name="logs")
    await logsChannel.send(f"<@{user.id}>: {message}")