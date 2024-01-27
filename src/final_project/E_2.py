import requests
import json
import openai
import os
import re

# Function to get game results from the college football data API
def get_game_results(api_key, year, week, season_type, team):
    base_url = "https://api.collegefootballdata.com/games"
    params = {
        'year': year,  # Year of the season
        'week': week,  # Week number
        'seasonType': season_type,  # Season type (e.g., regular, postseason)
        'team': team  # Team name
    }
    headers = {'Authorization': f'Bearer {api_key}'}  # Authorization header with API key

    response = requests.get(base_url, params=params, headers=headers)  # API request
    if response.status_code == 200:
        return response.json()  # Return JSON data if request is successful
    else:
        return f"Error: {response.status_code} - {response.reason}"  # Return error message

# Function to get team statistics from the college football data API
def get_team_stats(api_key, year, week, season_type, team):
    base_url = "https://api.collegefootballdata.com/games/teams"
    params = {
        'year': year,
        'week': week,
        'seasonType': season_type,
        'team': team
    }
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.reason}"

# Setting the OpenAI API key
openai.api_key = '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'

# Setting the API key for game data
game_data_api_key = 'Ey5Moh2ybLtcuTo+/KTFAt5/sX9URqFxk33GeG5Tu8xalAQ4FWyPKxXVlddnMeuO'

# Function to send a prompt to the OpenAI chat model and return its response
def get_openai_response(prompt):
    # Preparing the context for the AI (defining it as a helpful assistant)
    agent_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    # Sending the prompt to the OpenAI model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Using the GPT-3.5-turbo model
        messages=agent_prompt
    )

    # Extracting and returning the response from the AI
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message['content'].strip()
    else:
        return "No response from AI model."

# Function to parse the week number from the AI's response
def parse_week_number(ai_response):
    # Using regular expression to find a week number in the AI response
    match = re.search(r'week (\d+)', ai_response, re.IGNORECASE)
    if match:
        return int(match.group(1))  # Returning the week number if found
    else:
        return None  # Returning None if not found

# Function to process user queries
def process_query(query):
    # Getting the AI's interpretation of the user query
    ai_response = get_openai_response(query)
    
    # Extracting the week number from the AI response
    week_number = parse_week_number(ai_response)
    if week_number is None:
        return "I couldn't find the week number in the response."

    # Define the parameters for the API calls
    params = {
        'year': 2023,  # You can adjust these values as needed
        'week': week_number,
        'seasonType': 'regular',
        'team': 'Boise State'
    }

    # Fetch data based on the type of query
    if "game result" in ai_response or "team stats" in ai_response:
        data = None
        if "game result" in ai_response:
            data = get_game_results(game_data_api_key, params)
        elif "team stats" in ai_response:
            data = get_team_stats(game_data_api_key, params)

        # Construct a conversational summary
        summary = ""
        if data:
            if "game result" in ai_response:
                summary = f"In the game against {data[0]['home_team']} on {data[0]['start_date']}, Boise State scored {data[0]['away_points']} points while the home team scored {data[0]['home_points']} points."
            elif "team stats" in ai_response:
                summary = f"Boise State had {data[0]['stats'][0]['stat']} rushing touchdowns, {data[0]['stats'][1]['stat']} punt return yards, {data[0]['stats'][2]['stat']} punt return touchdowns, and more in their game on {data[0]['start_date']}."

        # Return the conversational summary
        return summary
    else:
        return "Sorry, I didn't understand your query."

# Welcome message for users
print("Welcome to the Boise State football chatbot!")
while True:
    # Taking user input
    user_query = input("What do you want to know about Boise State football? (Type 'exit' to quit): ")
    if user_query.lower() == 'exit':
        print("Goodbye!")
        break

    # Processing the query and printing the response
    response = process_query(user_query)
    if response:
        print(response)
