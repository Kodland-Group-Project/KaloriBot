import discord
import requests
import os
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")  

async def send_image(user, image_path):
    with open(image_path, 'rb') as img:
        file = discord.File(img)
        await user.send(file=file)

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f'''# Başlangıç/Yardım
Merhaba, {ctx.author.name}. Ben kalori yönetici bir botum.
''')

if __name__ == "__main__":
    bot.run(TOKEN)
