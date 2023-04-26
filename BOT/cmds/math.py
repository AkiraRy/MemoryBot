from discord.ext import commands

@commands.group()
async def math(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passsed}")

@math.command()
async def add(ctx, one : int, two : int):
    await ctx.send(one+two)
# automatically called when you load an extension
async def setup(bot):
    bot.add_command(math)
    #adds "add" directly
    bot.add_command(add)