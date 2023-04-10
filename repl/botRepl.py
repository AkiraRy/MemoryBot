import os
import random
import openai
import discord
from dotenv import load_dotenv
from keep_alive import keep_alive


load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
intents = discord.Intents.default()
intents.message_content = True
openai.api_key = os.environ['OPEN_AI']
CHANNEL_ID = int(os.environ['BOT_CHAT'])

class MemoryBot(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.get_channel(CHANNEL_ID).send('Hello, I am now online!')

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

        if message.content.lower() in greetings:
            response = random.choice(answers)
            await message.channel.send(response)

        #TODO  send <=5 pictures every day that were 1 week, 1 month,1 year ago on your choice
        if message.content.upper() == "CHAT ACTIVATIAN":
            await message.channel.send("---STARTING ACTIVATION---")

            #history = ''
            #print(history)
            #with open('./history.txt','r', encoding='utf-8') as f:
                #history = f.read()
            #history = history.replace('\n', ' ')
            #print(history)
            message_history = [
                #{"role": "system", "content": history},
                #{"role": "user", "content": "hi how is your day"},
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

    async def start_bot(self):
        try:
            await self.start(TOKEN)
        finally:
            await self.close()

    async def on_disconnect(self, message):
        print("stop")
        await message.channel.send('MemoryBot has been disconnected!')


client = MemoryBot(intents=intents)
keep_alive()
client.run(TOKEN)
