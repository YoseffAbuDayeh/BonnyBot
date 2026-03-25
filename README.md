# BonnyBot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.0+-5865F2?style=flat&logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

A Discord bot built in Python for managing and streamlining tournament streams. BonnyBot integrates with the **start.gg GraphQL API** to track live tournament set scores in real time and write them to a local text file — letting OBS pick them up automatically for clean, accurate scoreboard overlays without any manual input.

---

## Features

- **Live Score Tracker** — Polls the start.gg API every 3 seconds to detect the active set on a given stream. Scores update automatically as games are reported and are written to `Score.txt` for direct use as an OBS text source.
- **Smart Set Discovery** — Uses a two-phase discovery/tracking loop: first finds the active streamed set on a tournament event, then locks in and tracks it until it completes before searching for the next one.
- **AI Chat** — Conversational responses powered by the Cohere API.
- **Channel Management** — Commands to create Discord channels programmatically.
- **Command-gated** — Key commands are restricted to designated channels via a custom decorator.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| discord.py | Bot framework and command handling |
| start.gg GraphQL API | Live tournament and set data |
| Cohere API | AI-powered chat responses |
| asyncio | Non-blocking polling loop |
| python-dotenv | Secure API key management |

---

## How the Score Tracker Works

```
~stream <event_url> <streamer_name>
```

**Example:**
```
~stream https://www.start.gg/tournament/battle-on-the-horizon-5/event/ult-singles/brackets/... Up_N_Down
```

1. Parses the tournament and event slugs from the URL.
2. Resolves the event ID via the start.gg GraphQL API using fuzzy slug matching.
3. Starts an async polling loop that discovers the active set assigned to the given streamer's stream.
4. Once a set is found, tracks it directly by ID — posting score updates to Discord and overwriting `Score.txt` on every change.
5. When the set completes, clears the file and resumes discovery for the next set.

OBS reads `Score.txt` as a text source, giving streamers a fully automated, always-accurate scoreboard.

To stop tracking:
```
~stopstream
```

---

## Installation

```bash
git clone https://github.com/YoseffAbuDayeh/BonnyBot.git
cd BonnyBot
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
DISCORD_TOKEN=your_discord_bot_token
startgg=your_startgg_api_token
COHERE_API_KEY=your_cohere_api_key
```

Then run:
```bash
python bot.py
```

---

## Commands

| Command | Description |
|---|---|
| `~stream <event_url> <streamer>` | Start tracking a live tournament set for a given streamer |
| `~stopstream` | Stop the active score tracker |
| `~make <channel_name>` | Create a new Discord channel |

---

## Project Structure

```
BonnyBot/
├── bot.py                  # Entry point, bot setup
├── methods/
│   ├── ai.py               # Cohere chat integration
│   ├── commands.py         # General bot commands
│   └── method.py           # Shared utilities/helpers
├── ssb/
│   ├── stream.py           # start.gg integration and score tracker
│   └── cbs.py              # Additional tournament/stream logic
├── util/
│   └── decorators.py       # Channel restriction decorator
└── .env                    # API keys (not committed)
```
