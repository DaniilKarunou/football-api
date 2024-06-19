import streamlit as st
import pandas as pd
import plotly.express as px
from azure_functions.db_service import get_db
from azure_functions import models as ent


# Function to fetch player statistics from the database
def get_player_stats(player_id):
    session = get_db()
    player_stats = session().query(ent.PlayerSeasonStats) \
        .filter(ent.PlayerSeasonStats.player_id == player_id) \
        .order_by(ent.PlayerSeasonStats.season) \
        .all()
    player_stats_df = pd.DataFrame([stat.__dict__ for stat in player_stats])
    session().close()
    player_stats_df.drop_duplicates(inplace=True)  # Remove duplicates
    return player_stats_df


# Function to fetch unique player IDs and names
def get_player_ids():
    session = get_db()
    player_ids = session().query(ent.PlayerSeasonStats.player_id, ent.PlayerSeasonStats.player_name).distinct().all()
    player_ids_df = pd.DataFrame(player_ids, columns=["player_id", "player_name"])
    session().close()
    return player_ids_df


# Function to fetch detailed player information
def get_player_info(player_id):
    session = get_db()
    player_info = session().query(ent.PlayerSeasonStats).filter(ent.PlayerSeasonStats.player_id == player_id).first()
    session().close()
    return player_info


# Function to create UI elements using Streamlit
def create_ui(player_ids):
    st.sidebar.title("Choose a Player")
    player_id = st.sidebar.selectbox("Player ID", player_ids["player_id"], format_func=lambda x:
    player_ids.loc[player_ids['player_id'] == x, 'player_name'].values[0])

    return player_id


# Function to display statistics for a selected category
def show_statistics(player_stats, selected_category):
    stats_categories = {
        "Goals and Appearances": ["games_appearences", "goals_total"],
        "Passes": ["passes_total", "passes_accuracy"],
        "Dribbles": ["dribbles_attempts", "dribbles_success"],
        "Tackles": ["tackles_total", "fouls_committed"]
    }
    st.subheader(selected_category)
    stats_data = player_stats[["season"] + stats_categories[selected_category]].copy()  # Deep copy
    stats_data.sort_values(by="season", inplace=True)
    fig = px.line(stats_data, x="season", y=stats_data.columns[1:],
                  title=f"{selected_category} - Statistics by Season")
    st.plotly_chart(fig)


# Function to show the player information page
def show_player_info_page(player_info):
    st.title(f"Player Information: {player_info.player_name}")
    st.write(f"Age: {player_info.age}")
    st.write(f"Height: {player_info.height}")
    st.write(f"Weight: {player_info.weight}")
    st.write(f"Rating: {player_info.rating}")
    st.write(f"Games Appearances: {player_info.games_appearences}")
    st.write(f"Total Passes: {player_info.passes_total}")
    st.write(f"Pass Accuracy: {player_info.passes_accuracy}%")
    st.write(f"Dribble Attempts: {player_info.dribbles_attempts}")
    st.write(f"Dribble Success Rate: {player_info.dribbles_success}%")
    st.write(f"Total Tackles: {player_info.tackles_total}")
    st.write(f"Fouls Committed: {player_info.fouls_committed}")


# Main function to orchestrate the Streamlit app
def main():
    # Get unique player IDs
    player_ids = get_player_ids()

    # Streamlit UI
    page = st.sidebar.radio("Navigation", ["Player Statistics", "Player Information"])

    if page == "Player Statistics":
        player_id = create_ui(player_ids)
        player_stats = get_player_stats(player_id)

        # Define statistics categories
        stats_categories = {
            "Goals and Appearances": ["games_appearences", "goals_total"],
            "Passes": ["passes_total", "passes_accuracy"],
            "Dribbles": ["dribbles_attempts", "dribbles_success"],
            "Tackles": ["tackles_total", "fouls_committed"]
        }

        selected_category = st.sidebar.radio("Select Statistics Category", list(stats_categories.keys()))

        if selected_category in stats_categories:
            show_statistics(player_stats, selected_category)

    elif page == "Player Information":
        player_id = create_ui(player_ids)
        player_info = get_player_info(player_id)
        show_player_info_page(player_info)


if __name__ == "__main__":
    main()
