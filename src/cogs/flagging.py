import discord
from discord.ext import commands
from modules.profanity import testIfBad


class FlaggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dict = {} # should be populated from database

    @commands.command(name="flag", aliases=[ "report","abuse"])
    @commands.guild_only()
    async def _flag(self, ctx):
        replyId = ctx.message.reference
        if replyId is not None:
            replyMsg = await ctx.fetch_message(replyId.message_id)
            if replyMsg.author != self.bot.user:
                await ctx.message.delete()
                await ctx.author.send(f'Acknowledged new flag command.')
                check = testIfBad(replyMsg.content)
                await ctx.send(f'{ctx.author.mention} {check["message"]}')
            else:
                await ctx.send(f'{ctx.author.mention} You cannot flag a message from me.')
        else:
            await ctx.send(f'{ctx.author.mention} You must specify the flagged message by replying to it')


def setup(bot):
    bot.add_cog(FlaggingCog(bot))