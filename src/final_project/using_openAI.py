import openai
import os
import re
from game_results import get_game_results  # Module to get game results
from team_stats import get_team_stats      # Module to get team stats

# API keys for OpenAI and the game data source
openai.api_key = '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'

game_data_api_key = 'Ey5Moh2ybLtcuTo+/KTFAt5/sX9URqFxk33GeG5Tu8xalAQ4FWyPKxXVlddnMeuO'


def get_openai_response(prompt):
    """
    This function sends a prompt to the OpenAI chat model and returns its response.
    """
    # The agent prompt sets the context for the OpenAI model, describing its role
    agent_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    # Using the chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=agent_prompt
    )

    # Returning the AI's response
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message['content'].strip()
    else:
        return "No response from AI model."

def parse_week_number(ai_response):
    """
    This function parses the week number from the AI's response using regular expressions.
    """
    match = re.search(r'week (\d+)', ai_response, re.IGNORECASE)
    if match:
        return int(match.group(1))
    else:
        return None

def process_query(query):
    ai_response = get_openai_response(query)
    
    week_number = parse_week_number(ai_response)
    if week_number is None:
        return "I couldn't find the week number in the response."

    # Fetch data based on the type of query
    if "game result" in ai_response or "team stats" in ai_response:
        data = None
        if "game result" in ai_response:
            data = get_game_results(game_data_api_key, 2023, week_number, "regular", "Boise State")
        elif "team stats" in ai_response:
            data = get_team_stats(game_data_api_key, 2023, week_number, "regular", "Boise State")

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

# Example usage
user_query = "What was the outcome of Boise State's week 10 game"
response = process_query(user_query)
print(response)