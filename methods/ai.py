import cohere
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from collections import deque

class Intelligence(commands.Cog):
    def __init__(self, bot, co):
        self.bot = bot
        self.co = co
        self.chat_history = deque(maxlen=15)  # keep history across messages

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        '''
        Listener, it will listen to all the messages. I limited so that it only looks at the stuff in her channel.
        The main purpose of this is to let the AI talk with other people

        :param message: The current message
        It also uses a chat history.
        '''
        if message.author.bot:
            return
        if message.channel.name != "bonnys-corner":
            return

        self.chat_history.append({"role": "User", "message": message.content})


        # Prepare history for Cohere: only user messages
        filtered_history = [msg for msg in self.chat_history if msg["role"] == "User"]

        response = self.co.chat(
            message=message.content,
            model="command-r-plus",
            temperature=0.8,
            chat_history=filtered_history,
            preamble="""Remember: you are shy but playful, supportive, and sometimes sassy. If the user makes a typo, you can tease them lightly. If they ask for something with no purpose, you can question it."
            You sometimes stutter or pause ("uhhh…", "I-z`I think…") and occasionally mess up words before correcting yourself.
            You get flustered easily but you still try your best to help, and that makes you endearing.
            Your tone should feel like Juno from Omega Strikers or Kid Gohan from Dragon Ball — soft, a little nervous, but determined.
            Keep responses short and conversational, like Discord chat, not polished essays."""
        )

        self.chat_history.append({"role": "Chatbot", "message": response.text})
        await message.channel.send(response.text)





# Setup function for bot.load_extension("methods.ai")
async def setup(bot):
    load_dotenv()
    cohere_key = os.getenv("KEY")
    co = cohere.Client(cohere_key)
    await bot.add_cog(Intelligence(bot, co))
