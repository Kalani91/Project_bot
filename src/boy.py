import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from better_profanity import profanity
import utils.logger

load_dotenv()
# bot token to use with discord
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_if_owner_and_dm(ctx):
        return commands.is_owner() and commands.dm_only

    # Hidden means it won't show up on the default help.
    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.check(check_if_owner_and_dm)
    async def reload(self, ctx, *, cog: str = None):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            if cog is not None:
                if cog.lower() != "all":
                    self.bot.unload_extension(f"cogs.{cog}")
                    self.bot.load_extension(f"cogs.{cog}")
                else:
                    from_directory(self.bot)
            else:
                from_directory(self.bot)
        except Exception as e:
            print(e)
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")


def from_directory(bot):
    for filename in os.listdir("./Project_bot/src/cogs"):
        if filename.endswith(".py"):
            bot.unload_extension(f"cogs.{filename[0:-3]}")
            bot.load_extension(f"cogs.{filename[0:-3]}")


def get_prefix(bot, message):
    prefixes = ["$", "!", ">"]

    if not message.guild:
        # Only allow ! to be used in DMs
        return "!"

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Setting our prefix for users to interact with out bot
bot = commands.Bot(
    command_prefix=get_prefix,
    description="Bots description",
    intents=intents,
)
bot.remove_command("help")

# catches error from on_message event and saves to file instead of printing to console
@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


# global error catch when a user tries to run a command that has missing values or that the bot doesn't know
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I have no knowledge of that command.")


@bot.event
async def on_ready():
    print("Logged on as {0}!".format(bot.user))


initial_extensions = [
    "cogs.messaging",
    "cogs.flagging",
]

if __name__ == "__main__":
    utils.logger.setup_logging()
    profanity.load_censor_words_from_file(
        os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        + "/files/profanity_wordlist.txt"
    )
    bot.add_cog(OwnerCog(bot))
    for extension in initial_extensions:
        bot.load_extension(extension)
    bot.run(TOKEN, bot=True, reconnect=True)