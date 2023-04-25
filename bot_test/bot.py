from discord.ext import commands
import discord
import dotenv
import settings
from cogs.greetings import Greetings
from cogs.pictures import Pictures
dotenv.load_dotenv()
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents, heartbeat_interval=60.0)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        #print(f"User: {bot.user} (ID: {bot.user.id})")
        # kok loading
        #await bot.load_extension("cogs.greetings")
        #await bot.load_exten       sion("cogs.pictures")
        await bot.load_extension("cogs.pictures")


        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("handled error")

    @bot.command()
    async def picture(ctx):
        await bot.load_extension("cogs.pictures")

    @bot.command()
    async def unpicture(ctx):
        await bot.unload_extension("cogs.pictures")




    @bot.command()
    async def ping(ctx, waht):
        await ctx.send("pong")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()