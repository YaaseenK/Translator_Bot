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

    source_lang = translator.detect(message.content).lang

    for channel_name, target_lang in channel_language_map.items():
        if target_lang == source_lang:
            continue  # Don't re-post in same language

        channel = discord.utils.get(message.guild.text_channels, name=channel_name)
        if not channel:
            continue  # Skip if channel doesn't exist

        result = translator.translate(message.content, dest=target_lang)

        embed = discord.Embed(
            title="🌐 Universal Translation",
            description=f"**From ({source_lang}) ➡️ To ({target_lang})**\n\n**{result.text}**",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Original by {message.author.display_name} in #{message.channel.name}")
        await channel.send(embed=embed)

    # 🔧 This line ensures slash commands and other events still work
    await client.process_commands(message)


# Run the bot using your environment token
client.run(os.getenv("BOT_TOKEN"))
