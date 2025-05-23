import discord
from discord.ext import commands
from googletrans import Translator
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def translate(ctx, lang, *, text):
    translated = translator.translate(text, dest=lang)
    await ctx.send(f"**Translated ({lang}):** {translated.text}")

bot.run(os.getenv("BOT_TOKEN"))

