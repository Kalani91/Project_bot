from datetime import datetime
import discord
from discord.ext import commands
from better_profanity import profanity
from db.connector import db_instance
from db.tables import discord_channel, violated_message, clean_message, flagged_message
import requests

violation_limit = 3
ban_limit = 3

url = "https://community-purgomalum.p.rapidapi.com/containsprofanity"

headers = {
    "x-rapidapi-key": "8ca569a923mshb44f13cd2eb71f1p1442a2jsndefc10f14980",
    "x-rapidapi-host": "community-purgomalum.p.rapidapi.com",
}


class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db_instance.connect()
        self.channel_list = discord_channel.select()
        db_instance.close()

    # sends a direct message to user that joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        studentRole = discord.utils.get(member.guild.roles, name="student")
        await member.edit(roles=[studentRole])
        embed = discord.Embed(
            color=0x4A3D9A,
            title=f"Welcome to {member.guild.name}, {member.name}",
            description=f"By joining this server you agree to abide by the rules of the chat:",
        )
        embed.add_field(
            name="Be Concise and Brief",
            value="Keep messages brief, concise, and to the point. You can discuss anything unrelated afterwards.",
            inline=False,
        )
        embed.add_field(
            name="Avoid Caps Lock",
            value="Stick to sentence case. In the age of internet messaging, capitalized sentences are considered written shouting and sometimes irritating. Users  may think you’re rude, commanding, or angry at them.",
            inline=False,
        )
        embed.add_field(
            name="Be Patient Waiting for Feedback",
            value="Give people time to respond to your messages. Some users are slow typists, while others may be busy. You might not receive immediate feedback depending on the complexity of the issue at hand, either. Therefore, be patient and wait for the response instead of bombarding users with messages to get their attention.",
            inline=False,
        )
        embed.add_field(
            name="Don’t do Illegal Things",
            value="Streams, scamming people, harassing other users that kind of thing are not allowed",
            inline=False,
        )
        embed.add_field(
            name="No NSFW content",
            value="This is a public chat board, and as such there will be no content deemed to be not safe for work.",
            inline=False,
        )
        embed.set_footer(
            text=f"You joined the server on {datetime.now().strftime('%A, %d of %B, %Y at %H:%M:%S')}\n\nYou have been auto assigned as a STUDENT.\nif this is wrong, contact administrator."
        )
        await member.send(embed=embed)

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

        if isinstance(message.channel, discord.DMChannel):  # dm
            pass
        elif not message.guild:  # group dm
            pass
        else:  # guild
            check = profanityCheck(message.content)
            if check != "true":
                querystring = {"text": f"{message.content}"}
                check = requests.request(
                    "GET", url, headers=headers, params=querystring
                ).text

            db_instance.connect()

            if (message.channel.id, message.channel.name) not in self.channel_list:
                self.channel_list.append((message.channel.id, message.channel.name))
                discord_channel.insert(
                    message.channel.id,
                    message.channel.name,
                )

                author = message.author
            if check == "true":
                # save to database and delete message
                await message.delete()
                # message to channel
                await message.channel.send(
                        f"{author.mention} This message violates our server chat rules"
                )

                violated_message.insert(
                    message.id,
                        author.id,
                        author.name,
                    message.channel.id,
                    message.content,
                    message.content,
                    message.created_at,
                )

                userCount = violated_message.count_numbers_of_violation(
                    message.author.id
                )[0][0]
                    db_instance.close()

                # check if user has reached limit on violations
                    if author.guild_permissions.administrator == False:
                    if userCount % violation_limit == 0:
                        # check if user has reached threshold for total violations
                        if userCount / violation_limit >= ban_limit:
                                await author.send(
                                f"You have ignored the multiple warnings and have been banned from {message.guild.name}"
                            )
                                await author.ban(
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
                            await author.send(
                        )
                    else:
                        # send direct message to user
                            await author.send(
                            "Your message violates our terms of use and has been removed"
                        )
                else:
                    # admin violation
                        await author.send(
                        f"Your message violates our terms of use and has been removed,\nAs you are an administrator in {message.guild.name} your account bypasses the violation checks.\n\nTotal violations: {userCount}"
                    )
            else:
                clean_message.insert(
                    message.id,
                        author.id,
                        author.name,
                    message.channel.id,
                    message.content,
                    message.created_at,
                )
            db_instance.close()


# checking message for profanity
def profanityCheck(message):
    isProfain = profanity.contains_profanity(message)
    if isProfain:
        return "true"
    else:
        return "false"


def setup(bot):
    bot.add_cog(MessageCog(bot))