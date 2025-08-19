# 🤖 Discord Moderation Bot

A simple Discord moderation + utility bot built with [discord.py](https://discordpy.readthedocs.io/).  
Provides moderation tools, logging, and fun utilities to make server management easier.  

---

## ✨ Features

- 👋 Welcome new members automatically  
- 🗑️ Log deleted messages in a `#logs` channel  
- 🚫 Ban / unban members (`!ban`, `!unban`)  
- 🔇 Temporary mute with auto-unmute (`!mute`)  
- ⏰ Personal reminders (`!remindme`)  
- 📊 Server info (`!serverinfo`)  
- 👋 Friendly hello command (`!hello`)  

---

## 🛠️ Tech Stack
- [Python 3.10+](https://www.python.org/)  
- [discord.py](https://pypi.org/project/discord.py/)  
- [python-dotenv](https://pypi.org/project/python-dotenv/)  

---

## 📦 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/your-username/discord-mod-bot.git
   cd discord-mod-bot
   ```

2. **(Optional) Create a virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac
   .venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**  
   Create a `.env` file (do **not** commit this) with:  
   ```env
   DISCORD_TOKEN=your-bot-token-here
   ```

---

## ▶️ Running the Bot

```bash
python bot.py
```

When the bot is online, you should see in console:  
```
BotName#1234 is online in N server(s).
```

---

## 📜 Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!ban @user [reason]` | Ban a member | 🚫 Ban a user |
| `!unban username#1234` | Unban user | ✅ Remove ban |
| `!mute @user [minutes]` | Default 5 min | 🔇 Temporary mute |
| `!remindme <minutes> <task>` | `!remindme 10 drink water` | ⏰ Set a reminder |
| `!hello` | - | 👋 Simple greeting |
| `!serverinfo` | - | 📊 Show server details |

---

## ⚠️ Notes
- Ensure **Privileged Intents** (`MESSAGE CONTENT` and `SERVER MEMBERS`) are enabled in your Discord Developer Portal for the bot.  
- Do **not** commit your `.env` file with your bot token. Use `.env.example` instead.  

---

## 📄 License
MIT License © 2025  
