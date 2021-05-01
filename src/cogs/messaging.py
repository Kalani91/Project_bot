import discord
from discord.ext import commands
from better_profanity import profanity
from db.connector import db_instance
from db.tables import discord_channel, violated_message, clean_message, flagged_message

violation_limit = 3
ban_limit = 3

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

        check = profanityCheck(message.content)

        db_instance.connect()

        if check["profanity"] == True:
            # save to database and delete message
            await message.delete()
            # message to channel
            await message.channel.send(f'{message.author.mention} {check["message"]}')

            violated_message.insert(
                message.id,
                message.author.id,
                message.author.name,
                message.channel.id,
                message.content,
                message.content,
                message.created_at,
            )

            userCount = violated_message.count_numbers_of_violation(message.author.id)

            # check if user has reached limit on violations
            if(userCount % violation_limit == 0):
                # check if user has reached threshold for total violations
                if(userCount / violation_limit >= ban_limit):
                    # ban user from server
                    message.author.ban(reason='You have exceeded the maximum allowed violations and have been banned.',delete_message_days=7)
                else:
                    # kick/mute user
                    message.author.kick(reason='You have sent to many violations and have been kicked.')
            else:
                # send direct message to user
                await message.author.send("Your message was profain and has been removed")

        else:
            await message.reply(f'{message.author.mention} {check["message"]}')
            clean_message.insert(
                message.id,
                message.author.id,
                message.author.name,
                message.channel.id,
                message.content,
                message.created_at,
            )
        db_instance.close()


# checking message for profanity
def profanityCheck(message):
    isProfain = profanity.contains_profanity(message)
    if isProfain:
        return {
            "profanity": isProfain,
            "message": "This contains bad words.",
        }
    else:
        return {
            "profanity": isProfain,
            "message": "This does not contain bad words.",
        }


def setup(bot):
    bot.add_cog(MessageCog(bot))