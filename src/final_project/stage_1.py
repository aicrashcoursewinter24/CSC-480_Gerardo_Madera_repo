import pandas as pd
from datetime import datetime

def load_schedule(csv_file_path):
    # Reading the CSV file. 'parse_dates' is used to ensure the 'Start Date' column is treated as datetime objects
    df = pd.read_csv(csv_file_path, parse_dates=['Start Date'])
    return df

# def find_boise_state_games_by_date(schedule_df, input_date):
#     # Convert 'Start Date' directly to Boise's local time zone
#     schedule_df['Start Date'] = schedule_df['Start Date'].dt.tz_convert('America/Denver')

#     # Filtering for Boise State games on the specified date
#     boise_state_games = schedule_df[
#         ((schedule_df['Home Team'] == "Boise State") | (schedule_df['Away Team'] == "Boise State")) &
#         (schedule_df['Start Date'].dt.date == input_date)
#     ]

#     if not boise_state_games.empty:
#         for _, game in boise_state_games.iterrows():
#             start_time = game['Start Date'].strftime('%Y-%m-%d %I:%M %p %Z')
#             print(f"{game['Home Team']} vs {game['Away Team']} at {game['Venue']} on {start_time}")
#     else:
#         print("No games for Boise State on this date.")

# Function to find Boise State games by a specific week number      
def find_boise_state_game_by_week(schedule_df, week_number):
    # Filter the DataFrame for games where Boise State is either the home or away team in the specified week
    boise_state_games = schedule_df[
        ((schedule_df['Home Team'] == "Boise State") | (schedule_df['Away Team'] == "Boise State")) &
        (schedule_df['Week'] == week_number)
    ]

    # Check if there are any games for Boise State in the specified week
    if not boise_state_games.empty:
        # Iterate over each game found and print its details
        for _, game in boise_state_games.iterrows():
            # Format the start time of the game
            start_time = game['Start Date'].strftime('%Y-%m-%d %I:%M %p')
            # Determine if the game is a conference game
           # Updated condition to check if the 'Conference Game' column is 'true' (in lowercase)
            conference_game = "Conference" if str(game['Conference Game']).lower() == "true" else "Non-Conference"
            home_or_away = "Home" if game['Home Team'] == "Boise State" else "Away"
            print(f"Week {week_number} {game['Home Team']} vs {game['Away Team']} is a {home_or_away} {conference_game} game for Boise State at {game['Venue']} on {start_time} local standard time")
    else:
        # Print a message if no games are found for Boise State in the specified week
        print(f"No Boise State games found in week {week_number}.")

# Path to the CSV file - replace with the actual path to your file
csv_file_path = 'CSC-480/Porgect_CSC-480/final_project/boise_state_2023_schedule_data.csv'  # Replace with your file path

# Load the schedule from the CSV file
schedule_df = load_schedule(csv_file_path)

# Uncomment below lines attempting to search games by date
# input_date_str = input("Enter the date to check for games (YYYY-MM-DD): ")
# input_date = datetime.strptime(input_date_str, '%Y-%m-%d').date()

# find_boise_state_games_by_date(schedule_df, input_date)

# Prompt the user to enter a week number and find games for Boise State in that week
week_number = int(input("Enter the week number to check for games: "))
find_boise_state_game_by_week(schedule_df, week_number)




