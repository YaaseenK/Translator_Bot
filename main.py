# Import required libraries
import discord
from discord import app_commands  # For slash commands
from discord.ext import commands  # For bot setup
from googletrans import Translator  # Google Translate wrapper
import os  # For accessing environment variables

# Set up Discord bot intents (basic permissions)
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot
client = commands.Bot(command_prefix="/", intents=intents)

# Initialize the Google Translate API wrapper
translator = Translator()

# Mapping of channel names to their target language codes
channel_language_map = {
    "english-chat": "en",
    "french-chat": "fr",
    "spanish-chat": "es",
    "german-chat": "de",
    "portuguese-chat": "pt",
    "russian-chat": "ru",
    "chinese-chat": "zh-cn",
    "japanese-chat": "ja",
    "korean-chat": "ko",
    "hindi-chat": "hi"
}

# Event: Bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is online!")

    # Sync slash commands to Discord
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Slash command: /translate
@client.tree.command(name="translate", description="Translate text to another language")
@app_commands.describe(
    to="Language code to translate to (e.g., fr, es, de)",
    text="The text to translate"
)
async def translate(interaction: discord.Interaction, to: str, text: str):
    await interaction.response.defer()
    detected = translator.detect(text)
    result = translator.translate(text, dest=to)

    embed = discord.Embed(
        title="🌍 Translation",
        description=f"**Detected:** `{detected.lang}`\n**To:** `{to}`\n\n**Result:** {result.text}",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by YoPro's custom bot ✨")
    await interaction.followup.send(embed=embed)

# Universal translation for all messages in mapped channels
@client.event
async def on_message(message):
    if message.author.bot:
        return

    origin_channel_name = message.channel.name
    origin_language = channel_language_map.get(origin_channel_name)

    if not origin_language:
        return  # Only act in mapped language channels

    try:
        detected = translator.detect(message.content)
    except Exception as e:
        print(f"Detection failed: {e}")
        return

    # Translate to all other languages in other channels
    for target_channel_name, target_lang_code in channel_language_map.items():
        if target_channel_name == origin_channel_name:
            continue  # Skip origin channel

        try:
            result = translator.translate(message.content, dest=target_lang_code)

            embed = discord.Embed(
                title="🌍 Universal Translation",
                description=result.text,
                color=discord.Color.teal()
            )
            embed.set_footer(
                text=f"From #{origin_channel_name} | Detected: {detected.lang} → {target_lang_code}"
            )

            target_channel = discord.utils.get(message.guild.text_channels, name=target_channel_name)
            if target_channel:
                await target_channel.send(embed=embed)

        except Exception as e:
            print(f"Translation to {target_lang_code} failed: {e}")
            continue

# Run the bot using your environment token
client.run(os.getenv("BOT_TOKEN"))
