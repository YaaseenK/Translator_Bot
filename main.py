import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
import os

intents = discord.Intents.default()
client = commands.Bot(command_prefix="/", intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print(f"{client.user} is online!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@client.tree.command(name="translate", description="Translate text to another language")
@app_commands.describe(to="Language code to translate to (e.g., fr, es, de)", text="The text to translate")
async def translate(interaction: discord.Interaction, to: str, text: str):
    await interaction.response.defer()
    detected = translator.detect(text)
    result = translator.translate(text, dest=to)

    embed = discord.Embed(
        title=f"🌍 Translation",
        description=f"**Detected:** `{detected.lang}`\n**To:** `{to}`\n\n**Result:** {result.text}",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by your custom bot ✨")
    await interaction.followup.send(embed=embed)

client.run(os.getenv("BOT_TOKEN"))
