# Import required libraries
import discord
from discord import app_commands  # For slash commands
from discord.ext import commands  # For bot setup
from googletrans import Translator  # Google Translate wrapper
import os  # For accessing environment variables

# Set up Discord bot intents (basic permissions)
intents = discord.Intents.default()

# Initialize the bot with a command prefix (not used with slash commands, but still required)
client = commands.Bot(command_prefix="/", intents=intents)

# Initialize the Google Translate API wrapper
translator = Translator()

# Event: Bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is online!")

    # Try to sync slash commands to Discord's API
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Slash command: /translate
# Usage: /translate to:fr text:hello
@client.tree.command(name="translate", description="Translate text to another language")
@app_commands.describe(
    to="Language code to translate to (e.g., fr, es, de)",  # Slash command hint for target language
    text="The text to translate"  # Slash command hint for message content
)
async def translate(interaction: discord.Interaction, to: str, text: str):
    await interaction.response.defer()  # Acknowledge the interaction early (avoids timeout)

    # Detect the source language automatically
    detected = translator.detect(text)

    # Translate the text to the target language
    result = translator.translate(text, dest=to)

    # Build a clean Discord embed message
    embed = discord.Embed(
        title=f"🌍 Translation",
        description=f"**Detected:** `{detected.lang}`\n**To:** `{to}`\n\n**Result:** {result.text}",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by YoPro's custom bot ✨")

    # Send the translation back to the user
    await interaction.followup.send(embed=embed)

# Start the bot using the token stored in your environment variable
client.run(os.getenv("BOT_TOKEN"))
