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
        db_instance.connect()
        self.channel_list = discord_channel.select()
        db_instance.close()

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

        if isinstance(message.channel,discord.channel.DMChannel):  # dm
            pass
        elif not message.guild:  # group dm
            pass
        else:  # guild
            check = profanityCheck(message.content)

            db_instance.connect()

            if (message.channel.id, message.channel.name) not in self.channel_list:
                self.channel_list.append((message.channel.id, message.channel.name))
                discord_channel.insert(
                    message.channel.id,
                    message.channel.name,
                )

            if check["profanity"] == True:
                # save to database and delete message
                await message.delete()
                # message to channel
                await message.channel.send(
                    f'{message.author.mention} {check["message"]}'
                )

                violated_message.insert(
                    message.id,
                    message.author.id,
                    message.author.name,
                    message.channel.id,
                    message.content,
                    message.content,
                    message.created_at,
                )

                userCount = violated_message.count_numbers_of_violation(
                    message.author.id
                )[0][0]

                # check if user has reached limit on violations
                if message.author.guild_permissions.administrator == False:
                    if userCount % violation_limit == 0:
                        # check if user has reached threshold for total violations
                        if userCount / violation_limit >= ban_limit:
                            # ban user from server
                            await message.author.send(
                                f"You have ignored the multiple warnings and have been banned from {message.guild.name}"
                            )
                            await message.author.ban(
                                reason="Exceeded the maximum allowed violations in account.",
                                delete_message_days=7,
                            )
                        else:
                            # kick/mute user
                            await message.author.kick(
                                reason="Had to many violations and have been kicked."
                            )
                            await message.author.send("You have been kicked")
                    elif userCount % violation_limit == violation_limit - 1:
                        # warn user that they're on their final warning before being kicked
                        await message.author.send(
                            "If you ignore the server rules and continue to post messages that are deemed to violate our terms of use you will be kicked from the server."
                        )
                    else:
                        # send direct message to user
                        await message.author.send(
                            "Your message violates our terms of use and has been removed"
                        )
                else:
                    # admin violation
                    await message.author.send(
                        f"Your message violates our terms of use and has been removed,\nAs you are an administrator in {message.guild.name} your account bypasses the violation checks.\n\nTotal violations: {userCount}"
                    )
            else:
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