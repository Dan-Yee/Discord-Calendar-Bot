import json

# Imports for Discord API
import discord
from discord import user
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

# Setup the bot
intents = discord.Intents.none()
activity = discord.Activity(type = discord.ActivityType.listening, name = "Google Calendar")
bot = commands.Bot(command_prefix = "#", case_insensitive = True, activity = activity, status = discord.Status.online, intents = intents)
bot.remove_command("help")

# General variables
CONFIG_FILE_NAME = "config.json"

# API related variables
DISCORD_BOT_TOKEN = None                            # Stores the bot token for discord.py.
GOOGLE_CALENDAR_ID = None                           # The specific calendar being read using Google Calendar API.

# Bot settings
DISCORD_COMMANDS_REQUIRE_PERMISSION = None          # Flag to determine if any bot commands should enforce a role permission check. Default is True.
ALLOWED_ROLES = None                                # Discord roles that have permission to run bot commands.
DISCORD_ANNOUNCEMENT_CHANNEL_ID = None              # The Discord channel that the bot will send all messages to.
REMINDER_ROLES = None                               # Discord roles that will be pinged during reminder messages.
DISCORD_REMIND_BEFORE_EVENT_INTERVAL_MIN = None     # Number of minutes before an event's start time to send a reminder. Default is 30 minutes.
GOOGLE_CALENDAR_EVENT_CHECK_INTERVAL_MIN = None     # Number of minutes before sending another request to the Google Calendar API. Default is 1 hour.

"""
Reads the config file specified by CONFIG_FILE_NAME.
The config file contains required API keys and optional settings to configure the bot to function based on user needs.
"""
def load_config_file():
    global DISCORD_BOT_TOKEN, GOOGLE_CALENDAR_ID
    global DISCORD_COMMANDS_REQUIRE_PERMISSION, ALLOWED_ROLES, DISCORD_ANNOUNCEMENT_CHANNEL_ID, REMINDER_ROLES, DISCORD_REMIND_BEFORE_EVENT_INTERVAL_MIN, DISCORD_REMIND_BEFORE_EVENT_INTERVAL_MIN, GOOGLE_CALENDAR_EVENT_CHECK_INTERVAL_MIN

    config_file = open(CONFIG_FILE_NAME, "r")
    config = json.load(config_file)

    # Set API keys/tokens
    config_API = config.get("API", None)

    if config_API is None:
        raise Exception("Error reading API section of config.json.")
    else:
        DISCORD_BOT_TOKEN = config_API.get("DISCORD_BOT_TOKEN", None)
        GOOGLE_CALENDAR_ID = config_API.get("GOOGLE_CALENDAR_ID", None)

        if DISCORD_BOT_TOKEN is None:
            raise Exception("Error reading DISCORD_BOT_TOKEN in API section of config.json.")
        if GOOGLE_CALENDAR_ID is None:
            raise Exception("Error reading GOOGLE_CALENDAR_ID in API section of config.json.")

    # Set Bot settings
    config_SETTINGS = config.get("SETTINGS", None)

    if config_SETTINGS is None:
        raise Exception("Error reading SETTINGS section of config.json.")
    else:
        DISCORD_COMMANDS_REQUIRE_PERMISSION = config_SETTINGS.get("DISCORD_COMMANDS_REQUIRE_PERMISSION", True)
        ALLOWED_ROLES = set(config_SETTINGS.get("DISCORD_ALLOWED_ROLE_IDS", []))
        DISCORD_ANNOUNCEMENT_CHANNEL_ID = config_SETTINGS.get("DISCORD_ANNOUNCEMENT_CHANNEL_ID", None)
        REMINDER_ROLES = set(config_SETTINGS.get("DISCORD_REMINDER_ROLE_IDS", []))
        DISCORD_REMIND_BEFORE_EVENT_INTERVAL_MIN = config_SETTINGS.get("DISCORD_REMIND_BEFORE_EVENT_INTERVAL_MIN", 30)
        GOOGLE_CALENDAR_EVENT_CHECK_INTERVAL_MIN = config_SETTINGS.get("GOOGLE_CALENDAR_EVENT_CHECK_INTERVAL_MIN", 60)

    config_file.close()
    return

if __name__ == "__main__":
    try:
        load_config_file()
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as error:
        raise error