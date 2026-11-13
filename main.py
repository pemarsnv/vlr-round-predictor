from pprint import pprint

import requests

from round import Round

url = "http://127.0.0.1:3001/v2/match/logs"

response = requests.get(
    url,
    params={"match_id": 660386},
    timeout=60,
)
response.raise_for_status()

data = response.json()
game1 = data["data"]["segments"][0]
pprint(game1)
map_name = game1["map"]
team1_tag = game1["teams"]["team1"]["tag"]
team2_tag = game1["teams"]["team2"]["tag"]

for round_json in game1["rounds"]:

    round_atk_team = round_json["attacking_side"]
    round_def_team = "team2" if round_atk_team == "team1" else "team1"
    round_winner = round_json["winner"]
    round_economy = Round.compute_economy(round_json)
    round_team1score = round_json["score"]["team1"]
    round_team2score = round_json["score"]["team2"]

    round = Round(map_name, round_atk_team, round_def_team, round_winner, round_economy, round_team1score,
                   round_team2score, team1_tag, team2_tag)
    round.to_csv("rounds.csv")
