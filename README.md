# MemoryBot
A Bot that will rewoke your old memories


# Installation 
Use this code for https://replit.com/
(keep_alive.py and botReply.py)

1. Use pip install -r requirements.txt in a shell
2. Then add these 3 secret keys:
    1. BOT_CHAT - with the value of a discord chat where you want your bot to work
    2. DISCORD_TOKEN - with the token of your bot(you can find it on discord developer site)
    3. OPEN_AI - provide your API key if you want tou use chatgpt to talk with bot
3. If you want your bot to work for longer period of times use this site https://uptimerobot.com/ (it will ping your bot\`s site so it won\`t close after 1 hours of idle) 
4. Just hit the big green button at the top of your repl and you good to go

# Installation for local version

1. Repeat steps as for repl version
2. copy .env_sample as .env change accordingly
    -> one key difference is IMAGE_FOLDER variable, you need to provide path to img 
       so bot will be able to send some images from your local machine
3. in terminal run "python bot.py"


Local version update.log:

-> So far i`ve created a solid ground for my models to be used.
-> Going to leave this project for a while and do other stuff