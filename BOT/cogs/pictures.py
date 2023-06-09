import asyncio
import traceback
import discord
from discord.ext import commands
import os
import sys

sys.path.append(os.getenv('FOLDER_COGS'))
from plugins import *

async def is_botchat(ctx):
    return ctx.channel.id == int(os.getenv('BOT_CHAT'))

class Pictures(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_botchat)
    async def send_pic(self, ctx, type : str = "random", number : int = 5):
        print("here")
        if number >= 30:
            number = 5
        """
        :param ctx:
        :param type: random, google or path
        :return:
        """
        if type == "random":
            images_list = image_searcher(os.getenv('IMAGE_FOLDER'), number, rd=True)
            for images in images_list:
                await self.send_image(images, ctx.channel, spoiler=is_nsfw(images))
            await ctx.send(f"Successfully loaded {number} random images")
        elif type == "gmage":
            dict = search_folders()
            print(dict)
            # TODO add parameters to env, and use them to pic a folder
            my_folder = search_folderID(dict, 'Anime')
            filedic = search_files(my_folder, number=number)
            for items in filedic:
                print(items)
                await self.send_image(items['id'], ctx.channel, name=items['name'], google=True)
            await ctx.send(f"successfully loaded {number} gmages")
        # else:
        #     await self.send_image(type, ctx.channel, is_nsfw(type))

    async def send_image(self, image_path, channel, name="", spoiler=False, google=False):
        if google:
            # picture = discord.File(io.BytesIO(download_file(image_path)), filename=f"{image_path}.jpg")

            picture = discord.File(io.BytesIO(download_file(image_path)), filename=name)
            if spoiler:
                picture.spoiler = True
            try:
                await channel.send(file=picture)
            except Exception as e:
                print(traceback.format_exc())
                await channel.send("Files is too large")

        else:
            with open(image_path, 'rb') as f:
                picture = discord.File(f, filename=image_path.split("\\")[-1])
                if spoiler:
                    picture.spoiler = True
                try:
                    await channel.send(file=picture)
                except Exception as e:
                    print(traceback.format_exc())
                    await channel.send("Files is too large")

        await asyncio.sleep(3)




async def setup(bot):
    print("Pictures being loaded")
    await bot.add_cog(Pictures(bot))

async def teardown(bot):
    await bot.remove_cog(Pictures(bot))
    print('Pictures being unloaded!')