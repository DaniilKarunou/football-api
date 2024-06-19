import requests

from config import get_settings
from schemas import PlayerSeasonStats


def get_player_stats(player_id):
    url = f"{get_settings().api_url}/players/player/{player_id}"
    headers = {
        "x-rapidapi-host": get_settings().api_host,
        "x-rapidapi-key": get_settings().api_token,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        player_stats = data["api"]["players"]
        list_stats = []
        for player in player_stats:
            list_stats.append(get_stats_from_json(player))
        return list_stats
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def get_stats_from_json(player_stats):
    return PlayerSeasonStats(
        player_id=player_stats["player_id"],
        player_name=player_stats["player_name"],
        season=player_stats["season"],
        age=player_stats["age"],
        position=player_stats["position"],
        height=player_stats["height"],
        weight=player_stats["weight"],
        rating=player_stats["rating"],
        games_appearences=player_stats["games"]["appearences"],
        games_lineups=player_stats["games"]["lineups"],
        minutes_played=player_stats["goals"]["total"],
        goals_total=player_stats["goals"]["total"],
        passes_total=player_stats["passes"]["accuracy"],
        passes_accuracy=player_stats["passes"]["accuracy"],
        dribbles_attempts=player_stats["dribbles"]["attempts"],
        dribbles_success=player_stats["dribbles"]["success"],
        tackles_total=player_stats["tackles"]["total"],
        fouls_committed=player_stats["fouls"]["committed"]
    )
