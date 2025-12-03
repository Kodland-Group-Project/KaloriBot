import discord
import requests
import os
from logic import DBManager, calori_calculating
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
db = DBManager()

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

**Komutlar:**
- `!register <yaş> <boy(cm)> <kilo(kg)> <cinsiyet(1=kadın,2=erkek)>` - Kayıt ol
- `!set_goal <kalori>` - Günlük kalori hedefini ayarla
- `!add_calories <kalori>` - Kalori ekle
- `!status` - Günlük kalori durumunu göster
''')

@bot.command()
async def register(ctx: commands.Context, age: int, height: int, weight: int, gender: int):
    try:
        userid = ctx.author.id
        username = ctx.author.name
        db.add_user(userid, username, age, height, weight, gender)
        
        # Kalori hedefi hesapla
        bmr = calori_calculating(height, weight, age, gender)
        db.set_calories(userid, int(bmr))
        
        await ctx.send(f"✅ Kayıt başarılı, {username}! Günlük kalori hedefiniz: **{int(bmr)}** kcal")
    except Exception as e:
        await ctx.send(f"❌ Hata: {str(e)}")

@bot.command()
async def set_goal(ctx: commands.Context, calories: int):
    try:
        userid = ctx.author.id
        db.set_calories(userid, calories)
        await ctx.send(f"✅ Günlük kalori hedefiniz **{calories}** kcal olarak ayarlandı.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {str(e)}")

@bot.command()
async def add_calories(ctx: commands.Context, calories: int):
    try:
        userid = ctx.author.id
        db.add_calories(userid, calories)
        total = db.get_calories(userid)
        await ctx.send(f"✅ **{calories}** kcal eklendi. Toplam: **{total}** kcal")
    except Exception as e:
        await ctx.send(f"❌ Hata: {str(e)}")

@bot.command()
async def status(ctx: commands.Context):
    try:
        userid = ctx.author.id
        db.cursor.execute("SELECT aim_of_calories, total_calories FROM user WHERE userid = ?", (userid,))
        result = db.cursor.fetchone()
        
        if result:
            goal, total = result
            remaining = goal - total
            percentage = (total / goal * 100) if goal > 0 else 0
            
            await ctx.send(f"""
📊 **Kalori Durumu**
Hedef: {goal} kcal
Tüketilen: {total} kcal
Kalan: {remaining} kcal
İlerleme: {percentage:.1f}%
""")
        else:
            await ctx.send("❌ Lütfen önce `!register` komutu ile kayıt olun.")
    except Exception as e:
        await ctx.send(f"❌ Hata: {str(e)}")
    
if __name__ == "__main__":
    bot.run(TOKEN)
