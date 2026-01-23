from requests import get
from pprint import pprint

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

def get_links():
    try:
        data = get(BASE_URL + ALL_JSON).json()
        links = data['links']
        return links
    except Exception as e:
        print("Could not fetch NBA links. The API might be down or changed.")
        print("Error:", e)
        return None

def get_scoreboard():
    links = get_links()
    if not links:
        return
    
    scoreboard = links.get('currentScoreboard', None)
    if not scoreboard:
        print("No scoreboard available.")
        return

    try:
        games = get(BASE_URL + scoreboard).json()['games']
        
        for game in games:
            home_team = game['hTeam']
            away_team = game['vTeam']
            clock = game['clock']
            period = game['period']

            print("-------------------------------------------")
            print(f"{home_team['triCode']} vs {away_team['triCode']}")
            print(f"{home_team['score']} - {away_team['score']}")
            print(f"{clock} - {period['current']}")
            
    except Exception as e:
        print("Error fetching scoreboard details:", e)

print("Fetching NBA live scores...")
get_scoreboard()
