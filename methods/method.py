from discord.utils import get

async def DMsTexts(message, bot):
        '''
        This command is going to grab the message and put it on a specific channel. Used in-case someone DMs Bonny (the bot), which they shouldn't.

        params:
        ctx: This has all the data of the message, from the contents to the information about the channel.
        '''

        dms_channel = get(bot.get_all_channels(), name="dms")
        if dms_channel:
            await dms_channel.send(f"{message.author} ({message.author.id}) said: {message.content}")


# Logging events
async def LogEvent(user, bot, message):
    '''
    This method will log the events in the logs channel.

    params:
    user:       This variable has all the data of the user.
    bot:        This is the instance of the bot
    message:    This variable has the message of the action performed.
    '''
    logs_channel = get(bot.get_all_channels(), name="logs")
    if logs_channel:
        await logs_channel.send(f"<@{user.id}>: {message}")