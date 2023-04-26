import os

from discord.ext import commands
import discord
import dotenv
import settings
from cogs.greetings import Greetings
from cogs.pictures import Pictures
dotenv.load_dotenv()
logger = settings.logging.getLogger("bot")

count = 0


async def is_botchat(ctx):
    return ctx.channel.id == int(os.getenv('BOT_CHAT'))

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents, heartbeat_interval=60.0)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        #print(f"User: {bot.user} (ID: {bot.user.id})")
        # kok loading
        await bot.load_extension("cogs.pictures")
        await bot.load_extension("cogs.models")
        channel = bot.get_channel(int(os.getenv('BOT_CHAT')))
        await channel.send("Hello there")

        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument")

    @bot.command()
    @commands.check(is_botchat)
    async def reload_pictures(ctx):
        await bot.unload_extension("cogs.pictures")
        await bot.load_extension("cogs.pictures")

    @bot.command()
    @commands.check(is_botchat)
    async def reload_models(ctx):
        global count
        print(f"Reload number: {count}")
        count+=1
        await bot.unload_extension("cogs.models")
        await bot.load_extension("cogs.models")
        print("\n")


    @bot.command()
    @commands.check(is_botchat)
    async def ping(ctx, waht):
        await ctx.send("pong")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()