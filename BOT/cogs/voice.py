import discord
from discord.ext import commands
import os
import sys
import yt_dlp


sys.path.append(os.getenv('FOLDER_COGS'))
from plugins import *

async def is_botchat(ctx):
    return ctx.channel.id == int(os.getenv('BOT_CHAT'))

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_recorder = None

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice:
            print("cant join")
            return

        channel = ctx.message.author.voice.channel
        print(channel)
        await channel.connect()



    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if not voice_client:
            print("Not connected to a voice channel.")
            return

        await voice_client.disconnect()

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            print("Audio stopped.")
        else:
            print("No audio is currently playing.")

    @commands.command()
    async def play_youtube(self, ctx, youtube_link):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'nocheckcertificate': True,
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(youtube_link, download=False)
                    formats = info['formats']
                    audio_url = next((f['url'] for f in formats if f.get('acodec') == 'opus'), None)
                    if audio_url:
                        ffmpeg_opts = {
                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                            'options': '-vn',
                        }
                        source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts)
                        voice_client.play(source)
                        print(f"Now playing YouTube video: {youtube_link}")
                    else:
                        print("No compatible audio format found.")
                except yt_dlp.DownloadError as e:
                    print(f"An error occurred while downloading the audio: {str(e)}")
                except  Exception as e:
                    print(f"An error occurred while reading from the socket: {str(e)}")
        else:
            print("Not connected to a voice channel.")



async def setup(bot):
    print("Voice being loaded")
    await bot.add_cog(Voice(bot))

async def teardown(bot):
    await bot.remove_cog(Voice(bot))
    print('Voice being unloaded!')
