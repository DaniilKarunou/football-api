import azure.functions as func
import logging

import sqlalchemy as sa

from models import PlayerSeasonStats
from db_service import get_db
from football_api import get_player_stats

app = func.FunctionApp()


@app.timer_trigger(schedule="*/10 * * * * *", arg_name="timer", run_on_startup=False, use_monitor=False)
def process_football_api(timer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed.')

    player_ids = [184, 907, 278, 923, 874]
    player_stats = []

    session = get_db()()

    try:
        # Get the table object
        metadata = sa.MetaData()
        player_stats_table = sa.Table('player_season_stats', metadata, autoload_with=session.bind)

        # Clear the table
        delete_stmt = sa.delete(player_stats_table)
        session.execute(delete_stmt)

        # Commit the transaction to clear the table
        session.commit()

        # Get player statistics for multiple players
        for player_id in player_ids:
            stats = get_player_stats(player_id)
            if stats:
                player_stats.extend(stats)

        # Add new player statistics
        for stat in player_stats:
            player_stat = PlayerSeasonStats(
                player_id=stat.player_id,
                player_name=stat.player_name,
                season=stat.season,
                age=stat.age,
                height=stat.height,
                weight=stat.weight,
                rating=stat.rating,
                games_appearences=stat.games_appearences,
                games_lineups=stat.games_lineups,
                minutes_played=stat.minutes_played,
                goals_total=stat.goals_total,
                passes_total=stat.passes_total,
                passes_accuracy=stat.passes_accuracy,
                dribbles_attempts=stat.dribbles_attempts,
                dribbles_success=stat.dribbles_success,
                tackles_total=stat.tackles_total,
                fouls_committed=stat.fouls_committed
            )
            session.add(player_stat)

        session.commit()
        logging.info('Player statistics added to database.')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        session.rollback()

    finally:
        session.close()
