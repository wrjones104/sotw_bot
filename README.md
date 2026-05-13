# SotW Bot (Seed of the Week)

SotW Bot is a Discord bot designed to manage and automate "Seed of the Week" (SotW) events for the **Final Fantasy VI: Worlds Collide** (FF6WC) community. It handles community submissions, rolls new seeds automatically, manages leaderboards, and integrates with Google Sheets and the community website.

---

## 🚀 Key Features

- **Automated Rolling**: Automatically selects and rolls a new seed every Sunday at 00:00.
- **Community Submissions**: Allows users to submit their own flagsets for future SotW consideration.
- **Dynamic Leaderboards**: Tracks player finish times and forfeits, maintaining a live ranking in dedicated Discord channels.
- **Multi-Environment Support**: Seamlessly switches between `main` and `dev` API environments for seed generation.
- **Web Integration**: Syncs database data to Google Cloud Storage to power the community website's submission and leaderboard pages.
- **Chaos Mode**: Automatically rolls a chaotic seed if no community submissions are available.

---

## 🛠️ Slash Commands

The bot uses the `/sotw` command group:

| Command | Description |
| :--- | :--- |
| `/sotw submit` | Submit a new flagset idea for SotW consideration. |
| `/sotw done <time>` | Submit your finish time (format: `01:23:45`). |
| `/sotw forfeit` | Forfeit your run (cannot be undone). |
| `/sotw new` | (Admin) Manually create and roll a new SotW. |
| `/sotw force` | (Admin) Force the bot to auto-roll a new seed immediately. |
| `/sotw review` | (Admin) View the list of all pending submissions. |
| `/sotw refresh` | (Admin) Refresh the current SotW data and messages. |
| `/sotw auto <True/False>` | (Admin) Enable or disable the weekly auto-roll. |
| `/sotw reserve` | (Admin) Add a new reserve flagset to the backup list. |

---

## 💻 Developer Setup

### Prerequisites
- **Python 3.8+**
- A **Discord Bot** account with `Message Content` and `Server Members` intents enabled.
- A **Google Cloud Project** with the Google Sheets API enabled and a Service Account JSON key.

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sotw_bot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. **Environment Variables**: Create a `.env` file in the root directory with the following:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   GUILD_ID=your_discord_server_id
   SHEET_NAME=your_google_sheet_name
   SOTW_BOT_ENV=dev  # 'production' or 'dev'
   MAIN_API_KEY=your_ff6wc_main_api_key
   DEV_API_KEY=your_ff6wc_dev_api_key
   WEBAPP_API_KEY=your_website_integration_api_key
   ```

2. **Google Sheets Setup**:
   - Place your Google Service Account JSON key in the `functions/` directory.
   - Rename it to `sotw-bot-eda350e55a58.json` (or update the path in `functions/command_functions.py`).
   - Ensure the service account email has "Editor" access to your Google Sheet.

3. **Local Database**:
   - Ensure the `db/` directory exists.
   - The bot will automatically initialize `sotw_db.json`, `settings.json`, and `db/reserves.json` on first run if they don't exist.

---

## 🏗️ Tech Stack
- **Language**: Python
- **API Wrapper**: [discord.py](https://github.com/Rapptz/discord.py)
- **Sheet Integration**: [pygsheets](https://github.com/n67/pygsheets)
- **Storage**: Local JSON files + Google Cloud Storage (`gsutil`)
