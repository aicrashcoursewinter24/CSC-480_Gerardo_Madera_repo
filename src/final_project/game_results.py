import requests
import json

def get_game_results(api_key, year, week, season_type, team):
    base_url = "https://api.collegefootballdata.com/games"
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

# Example usage
api_key = 'Ey5Moh2ybLtcuTo+/KTFAt5/sX9URqFxk33GeG5Tu8xalAQ4FWyPKxXVlddnMeuO'  # Your API key
year = 2023
week = 10
season_type = 'regular'
team = 'Boise State'

game_results = get_game_results(api_key, year, week, season_type, team)
print(json.dumps(game_results, indent=4))
