from datetime import datetime
import discord
from discord.ext import commands
from db.connector import db_instance
from db.tables import flagged_message, violated_message

violation_limit = 3


class FlaggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db_instance.connect()
        self.dict = convert_from_db(flagged_message.select())
        db_instance.close()

    @commands.command(name="flag", aliases=["report", "abuse"])
    @commands.guild_only()
    async def _flag(self, ctx):
        replyId = ctx.message.reference
        author = ctx.author
        await ctx.message.delete()
        if replyId is not None:

            flagged_msg = await ctx.fetch_message(replyId.message_id)
            if flagged_msg.author != self.bot.user:

                if not flagged_msg.author.guild_permissions.administrator:

                    if (
                        # message has never been flaged before.
                        not flagged_msg.id in self.dict
                        # user has never flagged message before.
                        or author.id not in self.dict[flagged_msg.id]
                    ):

                        if not flagged_msg.id in self.dict:
                            self.dict.update({flagged_msg.id: [author.id]})
                        else:
                            self.dict[flagged_msg.id].append(author.id)

                        count = len(self.dict[flagged_msg.id])
                        muteRole = discord.utils.get(ctx.guild.roles, name="muted")

                        db_instance.connect()
                        flagged_message.insert(
                            flagged_msg.id,
                            author.id,
                            datetime.now().isoformat(),
                        )

                        if count >= violation_limit:
                            del self.dict[flagged_msg.id]
                            await flagged_msg.author.edit(roles=[muteRole])
                            await flagged_msg.delete()
                            await flagged_msg.author.send(
                                "Due to multiple users flagging your message, you have been muted.\nContact a staff member to re-enable your chat privileges."
                            )
                            violated_message.insert(
                                flagged_msg.id,
                                flagged_msg.author.id,
                                flagged_msg.author.name,
                                flagged_msg.channel.id,
                                flagged_msg.content,
                                flagged_msg.content,
                                flagged_msg.created_at,
                            )
                            flagged_message.delete(flagged_msg.id)
                        db_instance.close()

                    else:
                        await author.send(f"You can only flag a message once.")
                else:
                    await author.send(
                        f"You cannot flag staff member mesages as bad.\nIf you feel that {flagged_msg.author.mention} have abused chat rules. Send an email to Instatute admin: support@instatute.org, with a link to the message."
                    )
            else:
                await author.send(
                    f"{author.mention} You cannot flag a message from me."
                )
        else:
            await author.send(
                f"You must specify the flagged message by replying to it."
            )


def convert_from_db(db_data):
    data = dict()
    for flagged in db_data:
        if flagged[0] in data:
            data[flagged[0]].append(flagged[1])
        else:
            data.update({flagged[0]: [flagged[1]]})
    return data


def setup(bot):
    bot.add_cog(FlaggingCog(bot))