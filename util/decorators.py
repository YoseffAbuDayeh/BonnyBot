from discord.ext import commands
# Channel checking
def channel(channel_name):
    '''
    Checks if the data is in a specific channel.

    params:
    channel_name: This is the name of the channel that will be checked for

    returns:
    boolean: True if it was in the channel, false if not
    '''
    async def predicate(ctx):
        return ctx.guild and ctx.channel.name == channel_name
    return commands.check(predicate)

# Channel checking
def notChannel(channel_name):
    '''
    Checks if the data is in a specific channel.

    params:
    channel_name: This is the name of the channel that will be checked for

    returns:
    boolean: False if it was in the channel, true if not
    '''
    async def predicate(ctx):
        return ctx.guild and ctx.channel.name != channel_name
    return commands.check(predicate)


def notServer():
    '''
    Checks if the message sent is not in a server, this would mean that it is in a DM channel

    returns:
    boolean: True if it is in a DM channel, false if in a server
    '''
    async def predicate(ctx):
        return not ctx.guild
    return commands.check(predicate)
