import asyncio
import discord
from discord.ext import commands
import os
import openai
import sys
from discord.ui import Button

sys.path.append(os.getenv('FOLDER_COGS'))
from plugins import *


openai.api_key = os.getenv('OPEN_AI')

async def is_botchat(ctx):
    return ctx.channel.id == int(os.getenv('BOT_CHAT'))

class Models(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hist(self, ctx):
        history = ''
        path= "../history.txt" # this file needs to be in /bot folder
        with open(path, 'r', encoding='utf-8') as f:
            history = f.read()
        history = history.replace('\n', ' ')
        print(history)

        await ctx.send(history)

    @commands.command()
    @commands.check(is_botchat)
    async def activate(self, ctx, type : str = "gpt"):

        async def defaultGPT_click(interaction: discord.Interaction):
            await interaction.response.send_message('Default  ChatGPT activated: ')
            view = buttonGPT.view
            for item in view.children:
                item.disabled = True
            await interaction.message.edit(view=view)
            await self.chat_gpt(ctx)

        async def kurisuGPT_click(interaction: discord.Interaction):
            await interaction.response.send_message('KurisuGPT activated: ')
            view = kurisuGPT.view
            for item in view.children:
                item.disabled = True
            await interaction.message.edit(view=view)

            history = ''
            path = os.getenv('KURISU')
            with open(path, 'r', encoding='utf-8') as f:
                history = f.read()
            history = history.replace('\n', ' ')
            print(history)
            print(len(history.split(' ')))

            await self.chat_gpt(ctx, history=history)

        async def customGPT_click(interaction: discord.Interaction):
            await interaction.response.send_message('CustomGPT activated: ')
            view = customGPT.view
            for item in view.children:
                item.disabled = True
            await interaction.message.edit(view=view)

            message = await self.wait_for_message(ctx)
            if message == "" : return
            message = message.replace('\n', ' ')

            await self.chat_gpt(ctx, history=message)



        view = discord.ui.View()
        view.timeout = 20

        buttonGPT = Button(label='ChatGPT', custom_id='my_button', style=discord.ButtonStyle.primary)
        buttonGPT.callback = defaultGPT_click
        view.add_item(buttonGPT)

        kurisuGPT = Button(label='Kurisu', custom_id='kurisu', style=discord.ButtonStyle.success)
        kurisuGPT.callback = kurisuGPT_click
        view.add_item(kurisuGPT)

        customGPT = Button(label='Custom', custom_id='custom', style=discord.ButtonStyle.success)
        customGPT.callback = customGPT_click
        view.add_item(customGPT)


        await ctx.send('Choose your model:', view=view)

    async def wait_for_message(self, ctx):
        def check(m):
            return m.channel == ctx.channel and not m.author.bot

        try:
            await ctx.send("Enter your personality for ChatGPT under 50 words like this: ")
            await ctx.send("`You are not an assistant, your task is to roleplay as a character.\nCan you talk to me as if you are this character? Please only provide short answers around 15 words and try not to break out of character.` Here's her description: 'here!'  ")

            message = await self.bot.wait_for('message', check=check, timeout=60.0)
            if len(message.content.split(' ')) > 50 :
                await ctx.send("Your personality was to long, try again with !activate")
                return ""

            return message.content
        except asyncio.TimeoutError:
            await ctx.send("timeout for message")
            print("timeout for message")

    async def chat_gpt(self, ctx, history=""):


        await ctx.send("launching")
        message_history = [
            {"role": "system", "content": history},
            {"role": "user", "content": history},

        ]
        # {"role": "system", "content": history},
        # {"role": "user", "content": "hi how is your day"},
        while True:
            messages = (
                await ctx.bot.wait_for('message', check=lambda m: m.author == ctx.author)).content.lower()
            if messages == "stop":
                await ctx.channel.send("---ACTIVATION STOPPED---")
                break

            message_history.append({"role": "user", "content": messages})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )
            print(response)
            message_history.append({"role": "assistant", "content": response.choices[0].message.content})
            await ctx.channel.send(response.choices[0].message.content)




async def setup(bot):
    print("Models being loaded")
    await bot.add_cog(Models(bot))

async def teardown(bot):
    await bot.remove_cog(Models(bot))
    print('Models being unloaded!')