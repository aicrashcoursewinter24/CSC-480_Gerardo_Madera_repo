import pandas as pd
import requests  # You'll need to import the requests library for API calls

def load_schedule(csv_file_path):
    df = pd.read_csv(csv_file_path, parse_dates=['Start Date'])
    return df

def find_boise_state_game_by_week(schedule_df, week_number):
    boise_state_games = schedule_df[
        ((schedule_df['Home Team'] == "Boise State") | (schedule_df['Away Team'] == "Boise State")) &
        (schedule_df['Week'] == week_number)
    ]

    if not boise_state_games.empty:
        for _, game in boise_state_games.iterrows():
            start_time = game['Start Date'].strftime('%Y-%m-%d %I:%M %p')
            conference_game = "Conference" if str(game['Conference Game']).lower() == "true" else "Non-Conference"
            home_or_away = "Home" if game['Home Team'] == "Boise State" else "Away"
            print(f"Week {week_number} {game['Home Team']} vs {game['Away Team']} is a {home_or_away} {conference_game} game for Boise State at {game['Venue']} on {start_time} local standard time")
    else:
        print(f"No Boise State games found in week {week_number}.")

def query_openai_nlu(query):
    # Define your OpenAI API endpoint, headers, and data
    endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": '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'  # Replace with your OpenAI API key
    }
    data = {
        "prompt": query,
        "max_tokens": 50  # Adjust the max tokens as needed
    }

    # Make the API request to OpenAI
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("API request failed.")
        return None

# Path to the CSV file - replace with the actual path to your file
csv_file_path = 'CSC-480/Porgect_CSC-480/final_project/boise_state_2023_schedule_data.csv'  # Replace with your file path

# Load the schedule from the CSV file
schedule_df = load_schedule(csv_file_path)

# Prompt the user to enter a week number and find games for Boise State in that week
week_number = int(input("Enter the week number to check for games: "))
find_boise_state_game_by_week(schedule_df, week_number)

# Example user query input
user_query = input("Ask a question: ")

# Query OpenAI NLU
nlu_response = query_openai_nlu(user_query)

if nlu_response:
    answer = nlu_response["choices"][0]["text"]
    print(answer)
