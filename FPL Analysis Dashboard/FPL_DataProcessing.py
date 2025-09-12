import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer
import requests
import logging

'''
# Load from dataset
file_path = 'Players_data_23-24.csv'  # Update with your file path
players_data = pd.read_csv(file_path)
'''
##################################################### Logger ##################################################### 
# Setup logging
logging.basicConfig(level=logging.INFO)

##################################################### Get the Data ##################################################### 

# Function to fetch and process the data
def fetch_fpl_data():
    try:
        # Convert each key to a DataFrame
        # Step 1: Gather Data
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        data = response.json()

        # Step 2: Convert each key to a DataFrame
        players_df       = pd.DataFrame(data['elements'])
        events_df        = pd.DataFrame(data['events'])
        game_settings_df = pd.DataFrame([data['game_settings']])
        phases_df        = pd.DataFrame(data['phases'])
        teams_df         = pd.DataFrame(data['teams'])
        elements_df      = pd.DataFrame(data['elements'])
        element_stats_df = pd.DataFrame(data['element_stats'])
        element_types_df = pd.DataFrame(data['element_types'])

        # Step 3: Merge players_df with element_types_df on 'element_type'
        players_with_positions = pd.merge(players_df, element_types_df, left_on='element_type', right_on='id', suffixes=('_player', '_type'))

        # Step 4: Data PreProcessing
        players_with_positions['now_cost'] = players_with_positions['now_cost']/10
        players_with_positions["expected_goals"] = pd.to_numeric(players_with_positions["expected_goals"], errors='coerce')
        players_with_positions = pd.merge(players_with_positions, teams_df, left_on='team', right_on='id', how='left',suffixes = ('_Player','_Team'))

        return players_with_positions

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from the API: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during data processing: {e}")
        return None


##################################################### main function ##################################################### 
# Main execution block
if __name__ == "__main__":
    players_data = fetch_fpl_data()
    if players_data is not None:
        logging.info("Data processed successfully!")
        # Optionally save or use the data further here
    else:
        logging.error("Failed to fetch or process data.")