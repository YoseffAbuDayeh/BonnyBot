import os
from discord.ext import commands
from util import decorators
import asyncio
import re
import requests
from dotenv import load_dotenv
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCORE_FILE = BASE_DIR / "Score.txt"


load_dotenv()
API_TOKEN = os.getenv("startgg")
API_URL = "https://api.start.gg/gql/alpha"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


def parse_event_slug(url: str):
    match = re.search(r"start\.gg/tournament/([^/]+)/event/([^/]+)", url)
    if not match:
        raise ValueError("Invalid start.gg event URL")
    return match.group(1), match.group(2)

def normalize(text: str) -> str:
    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("singles", "")
        .strip()
    )


def get_event_id(tournament_slug: str, url_event_slug: str) -> int:
    query = """
    query TournamentEvents($slug: String!) {
      tournament(slug: $slug) {
        events {
          id
          name
          slug
        }
      }
    }
    """

    res = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": query, "variables": {"slug": tournament_slug}},
        timeout=10
    )

    payload = res.json()

    if "data" not in payload:
        if "errors" in payload:
            messages = ", ".join(e["message"] for e in payload["errors"])
            raise RuntimeError(f"API error while fetching tournament: {messages}")
        raise RuntimeError("Unknown API error (no data returned)")

    tournament = payload["data"].get("tournament")
    if not tournament:
        raise RuntimeError("Tournament not found")

    events = tournament.get("events")
    if not events:
        raise RuntimeError("No events found in tournament")

    norm_url = normalize(url_event_slug)

    for e in events:
        if e["slug"] == url_event_slug:
            return e["id"]

    for e in events:
        if normalize(e["name"]) == norm_url:
            return e["id"]

    for e in events:
        if norm_url in normalize(e["name"]):
            return e["id"]

    raise RuntimeError("Could not match event from URL")


def fetch_onstream_sets(event_id: int):
    query = """
    query OnStreamSets($eventId: ID!) {
      event(id: $eventId) {
        sets(perPage: 50, sortType: RECENT) {
          nodes {
            id
            startedAt
            completedAt
            stream {
              streamName
            }
            slots {
              entrant {
                id
                name
              }
            }
            games {
              winnerId
            }
          }
        }
      }
    }
    """

    try:
        res = requests.post(
            API_URL,
            headers=HEADERS,
            json={"query": query, "variables": {"eventId": event_id}},
            timeout=10
        )
        payload = res.json()
    except Exception:
        return []

    # GraphQL errors-only response
    if "data" not in payload:
        return []

    event = payload["data"].get("event")
    if not event:
        return []

    sets = event.get("sets")
    if not sets:
        return []

    nodes = sets.get("nodes")
    if not nodes:
        return []

    return nodes




def print_scores_discord(sets, streamer_name, last_scores, channel):
    OUTPUT_FILE = SCORE_FILE

    # Filter sets for the correct streamer
    streamer_sets = [
        s for s in (sets or [])
        if isinstance(s, dict)
        and s.get("stream")
        and s["stream"].get("streamName")
        and normalize(streamer_name) in normalize(s["stream"]["streamName"])
    ]

    # Find the active set (started but not completed)
    # Find the most recently started active set
    active_sets = [
        s for s in streamer_sets
        if s.get("startedAt") and not s.get("completedAt")
    ]

    if not active_sets:
        return last_scores

    # Pick the most recently started set
    active_set = max(active_sets, key=lambda s: s["startedAt"])

    if not active_set:
        return last_scores

    slots = active_set.get("slots") or []
    if len(slots) != 2:
        return last_scores

    p1 = slots[0].get("entrant") or {}
    p2 = slots[1].get("entrant") or {}
    if not p1 or not p2:
        return last_scores

    # Count games
    p1_score = 0
    p2_score = 0
    for g in active_set.get("games") or []:
        if not g:
            continue
        if g.get("winnerId") == p1.get("id"):
            p1_score += 1
        elif g.get("winnerId") == p2.get("id"):
            p2_score += 1

    set_id = active_set.get("id")
    if last_scores.get(set_id) != (p1_score, p2_score):
        score_text = f"{p1.get('name','?')} {p1_score} – {p2_score} {p2.get('name','?')}"

        # Send to Discord
        asyncio.create_task(
            channel.send(f"**{score_text}**")
        )

        # Write to OBS text file
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(score_text)
        except Exception as e:
            asyncio.create_task(
                channel.send(f"⚠️ Failed to write score file: `{e}`")
            )

        last_scores[set_id] = (p1_score, p2_score)

    return last_scores

def fetch_set_by_id(set_id: int):
    query = """
    query SetById($setId: ID!) {
      set(id: $setId) {
        id
        startedAt
        completedAt
        stream {
          streamName
        }
        slots {
          entrant {
            id
            name
          }
        }
        games {
          winnerId
        }
      }
    }
    """

    try:
        res = requests.post(
            API_URL,
            headers=HEADERS,
            json={"query": query, "variables": {"setId": set_id}},
            timeout=10
        )
        payload = res.json()
    except Exception:
        return None

    return payload.get("data", {}).get("set")


def discover_streamed_set(event_id: int, streamer_name: str, max_pages=5):
    for page in range(1, max_pages + 1):
        sets = fetch_onstream_sets(event_id)

        for s in sets:
            if not s.get("stream"):
                continue
            if normalize(streamer_name) not in normalize(s["stream"]["streamName"]):
                continue
            if not s.get("startedAt"):
                continue
            if s.get("completedAt"):
                continue

            return s  # 🎯 FOUND

    return None


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker_task = None
        self.tracker_running = False

    async def stream_tracker(self, channel, event_id, streamer_name):
        OUTPUT_FILE = r"D:/Score.txt"
        last_scores = {}
        active_set_id = None

        await channel.send(f"**Tracking `{streamer_name}` on start.gg**")

        while self.tracker_running:
            try:
                # 🔍 DISCOVERY PHASE
                if active_set_id is None:
                    discovered = await asyncio.to_thread(
                        discover_streamed_set, event_id, streamer_name
                    )

                    if discovered:
                        active_set_id = discovered["id"]
                        last_scores.clear()
                        await channel.send("**Stream set detected — locking in**")

                    await asyncio.sleep(3)
                    continue

                # 🎯 TRACKING PHASE
                current_set = await asyncio.to_thread(fetch_set_by_id, active_set_id)

                if not current_set:
                    active_set_id = None
                    continue

                if current_set.get("completedAt"):
                    # Clear OBS file
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        f.write("")

                    await channel.send("**Stream set finished — waiting for next set**")
                    active_set_id = None
                    last_scores.clear()
                    await asyncio.sleep(3)
                    continue

                # Update scores
                last_scores = print_scores_discord(
                    [current_set], streamer_name, last_scores, channel
                )

            except Exception as e:
                await channel.send(f"Error: `{e}`")

            await asyncio.sleep(3)

    @commands.command()
    @decorators.channel("stream-to")
    async def stream(self, ctx, event_url: str, streamer: str):
        if self.tracker_running:
            await ctx.send("Tracker already running.")
            return

        try:
            t_slug, e_slug = parse_event_slug(event_url)
            event_id = get_event_id(t_slug, e_slug)

        except Exception as e:
            await ctx.send(f"{e}")
            return

        self.tracker_running = True
        self.tracker_task = asyncio.create_task(
            self.stream_tracker(ctx.channel, event_id, streamer)
        )

        await ctx.send("Stream tracker started.")

    @commands.command()
    @decorators.channel("stream-to")
    async def stopstream(self, ctx):
        if not self.tracker_running:
            await ctx.send("No tracker running.")
            return

        self.tracker_running = False
        if self.tracker_task:
            self.tracker_task.cancel()

        await ctx.send("Stream tracker stopped.")

# Setup function for
# bot.load_extension("methods.ai")
async def setup(bot):
    load_dotenv()
    API_TOKEN = os.getenv("startgg")
    await bot.add_cog(Stream(bot))

