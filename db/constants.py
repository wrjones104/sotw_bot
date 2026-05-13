import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration (production or dev)
# This determines which sheet and guild the bot instance interacts with.
BOT_ENV = os.getenv("SOTW_BOT_ENV", "dev")

# Discord & Guild settings are now instance-specific in .env
discord_token = os.getenv("DISCORD_TOKEN")
guild = int(os.getenv("GUILD_ID", "0"))
sheetname = os.getenv("SHEET_NAME")
env_type = BOT_ENV

# API Configuration - Both are available to both bots for cross-environment rolling
FF6WC_APIS = {
    "main": {
        "url": "https://api.ff6worldscollide.com/api/seed",
        "key": os.getenv("MAIN_API_KEY")
    },
    "dev": {
        "url": "https://devapi.ff6worldscollide.com/api/seed",
        "key": os.getenv("DEV_API_KEY")
    }
}

# Default API to use if none is specified
DEFAULT_API = "main"

webapp_api_key = os.getenv("WEBAPP_API_KEY")