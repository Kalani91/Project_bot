import discord
from discord.ext import commands
from modules.profanity import testIfBad


class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dict = {}

    # sends a direct message to user that joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Hi {member.name}, welcome to our discord server!"
        )

    # on message event run anytime someone posts a message to a channel
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # prints all messages to console
        print(
            'In channel "{0.guild}.{0.channel}" - Message from {0.author.name}: {0.content}'.format(
                message
            )
        )
        # checks if a user is saying hello to the bot and returns the favour
        if "hello" in message.content.lower():
            if self.bot.user.mentioned_in(message):
                response = "Hello to you too {0.author.mention}".format(message)
                await message.channel.send(response)

        check = testIfBad(message.content)
        print(check)
        print(check["profanity"] == True)
        if check["profanity"] == True:
            # save to database and delete message
            await message.delete()
            # message to channel
            await message.channel.send(f'{message.author.mention} {check["message"]}')

            # send direct message to user
            await message.author.send("Your message was profain and has been removed")
        else:
            await message.reply(f'{message.author.mention} {check["message"]}')


def setup(bot):
    bot.add_cog(MessageCog(bot))