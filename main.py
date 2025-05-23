# Import required libraries
import discord
from discord import app_commands  # For slash commands
from discord.ext import commands  # For bot setup
from googletrans import Translator  # Google Translate wrapper
import os  # For accessing environment variables

# Set up Discord bot intents (basic permissions)
intents = discord.Intents.default()
intents.message_content = True

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

# Mapping of channel names to their target language codes
channel_language_map = {
    "french-chat": "fr",
    "spanish-chat": "es",
    "german-chat": "de",
    "portuguese-chat": "pt",
    "russian-chat": "ru",
    "chinese-chat": "zh-cn",
    "japanese-chat": "ja",
    "korean-chat": "ko",
    "hindi-chat": "hi",
    "english-chat": "en"
}

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author.bot:
        return

    # Get the target language from the channel name
    target_lang = channel_language_map.get(message.channel.name)

    # Only act in mapped language channels
    if target_lang:
        # Detect source language
        detected = translator.detect(message.content)

        # If the message is already in the target language, do nothing
        if detected.lang == target_lang:
            return

        # Translate to the channel’s target language
        result = translator.translate(message.content, dest=target_lang)

        # Format and send an embed with the translation
        embed = discord.Embed(
            title=f"🌐 Auto-Translation",
            description=(
                f"**From:** `{detected.lang}`\n"
                f"**To:** `{target_lang}`\n\n"
                f"**Result:** {result.text}"
            ),
            color=discord.Color.orange()
        )
        embed.set_footer(text="Auto-translated by YoPro’s bot ✨")
        await message.channel.send(embed=embed)


# Start the bot using the token stored in your environment variable
client.run(os.getenv("BOT_TOKEN"))
