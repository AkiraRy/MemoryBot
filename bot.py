import asyncio
import os
import random
import openai
import discord
from dotenv import load_dotenv
from plugins import is_nsfw, image_searcher
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
openai.api_key = os.getenv('OPEN_AI')
CHANNEL_ID = int(os.getenv('BOT_CHAT'))


class MemoryBot(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.get_channel(CHANNEL_ID).send('Hello, I am now online!')

    # noinspection PyTypeChecker
    async def on_message(self, message):
        if message.author == self.user:
            return

        greetings = [
            'hi memorybot',
            'hello memorybot',
            'what`s up memory',
        ]
        answers = [
            'Hello there ' + message.author.name + '!',
            'Hello ' + message.author.name + '!',
            'Good, how are you ' + message.author.name + '?',
        ]
        if message.content.startswith('^botservers'):
            await message.channel.send(f"I'm in {len(client.guilds)} servers!")

        if message.content.lower() in greetings:
            response = random.choice(answers)
            await message.channel.send(response)

        if message.content.lower() == "send image":
            await message.channel.send("Do you give me path or i send you images?")

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            try:
                path_msg = await client.wait_for('message', timeout=30.0, check=check)
                msg = path_msg.content

                if msg == 'send me random':
                    images_list = image_searcher(os.getenv('IMAGE_FOLDER'), 5, rd=True)
                    for images in images_list:
                        await self.send_pic(images, message.channel, is_nsfw(images))

                else:
                    await self.send_pic(msg, message.channel, is_nsfw(msg))
            except asyncio.TimeoutError:
                await message.channel.send('You took too long to reply.')

        if message.content.lower() == "send folder of images":
            await message.channel.send("What is the path to a picture?")

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            try:
                path_msg = await client.wait_for('message', timeout=30.0, check=check)
                path = path_msg.content

                with open(path, 'rb') as f:
                    picture = discord.File(f)
                    await message.channel.send(file=picture)

            except asyncio.TimeoutError:
                await message.channel.send('You took too long to reply.')

        # memory activation send <=5 pictures every day that were 1 year ago or more ago
        if message.content.upper() == "CHAT ACTIVATIAN":
            await message.channel.send("---STARTING ACTIVATION---")

            history = ''
            print(history)
            with open('./history.txt', 'r', encoding='utf-8') as f:
                history = f.read()
            # history = history.replace('\n', ' ')
            print(history)
            message_history = [
                {"role": "system", "content": history},
                {"role": "user", "content": "hi how is your day"},
            ]
            # {"role": "system", "content": history},
            # {"role": "user", "content": history},

            while True:
                messages = (
                    await self.wait_for('message', check=lambda m: m.author == message.author)).content.lower()
                if messages == "stop":
                    await message.channel.send("---ACTIVATION STOPPED---")
                    break

                message_history.append({"role": "user", "content": messages})
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message_history
                )
                print(response)
                message_history.append({"role": "assistant", "content": response.choices[0].message.content})
                await message.channel.send(response.choices[0].message.content)

    # noinspection PyTypeChecker
    async def send_pic(self, image_path, channel, spoiler=False):
        with open(image_path, 'rb') as f:
            picture = discord.File(f)
            if spoiler:
                picture = discord.File(f, spoiler=spoiler)
            try:
                await channel.send(file=picture)
            except:
                await channel.send("Files is too large")

        time.sleep(3)

    async def on_disconnect(self, message):
        print("stop")
        await message.channel.send('MemoryBot has been disconnected!')


client = MemoryBot(intents=intents)
client.run(TOKEN)
