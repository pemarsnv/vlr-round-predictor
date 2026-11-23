import time
import re
from pprint import pprint

import requests

from round import Round

TIER_1_PATTERNS = [
    r"VCT \d{4}: Americas",
    r"VCT \d{4}: EMEA",
    r"VCT \d{4}: Pacific",
    r"VCT \d{4}: China",
    "Valorant Masters",
    r"Valorant Champions \d{4}",
    r"Champions Tour",
]


def is_tier_1(event):
    return any(
        re.search(pattern, event["title"])
        for pattern in TIER_1_PATTERNS
    )


def get_all_events():
    url = "http://127.0.0.1:3001/v2/events"
    vct_events = []
    response = []

    for page in range(1, 101):
        request_success = False
        tries = 0

        while tries < 10:
            response = requests.get(
                url,
                params={
                    "q": "completed",
                    "page": page
                },
                timeout=60,
            )

            if response.status_code == 429:
                tries += 1
                print(f"Rate limited on page {page}. Retry {tries}/10")

                time.sleep(5)
                continue

            response.raise_for_status()
            request_success = True
            break

        if not request_success:
            print(f"Giving up on page {page}.")
            continue

        data = response.json()["data"]["segments"]

        for event in data:
            if is_tier_1(event):
                vct_events.append(event)

        print(f"Page {page}/100 processed")

    return vct_events


def get_all_matches_ids_from_events(vct_events):
    url = "http://127.0.0.1:3001/v2/events/matches"
    vct_matches_ids = []
    response = []

    for event in vct_events:
        event_id = event["event_id"]
        request_success = False
        tries = 0

        while tries < 10:
            response = requests.get(
                url,
                params={"event_id": event_id},
                timeout=60,
            )

            if response.status_code == 429:
                tries += 1
                print(f"Rate limited on event {event_id}. Retry {tries}/10")
                time.sleep(5)
                continue

            response.raise_for_status()
            request_success = True
            break

        if not request_success:
            print(f"Giving up on event {event_id}.")
            continue

        data = response.json()["data"]["segments"]

        for match in data:
            vct_matches_ids.append(match["match_id"])

        print(f"Event {event_id} processed")

    return vct_matches_ids


def get_all_rounds_from_matches(matches_ids):
    url = "http://127.0.0.1:3001/v2/match/logs"

    for match_id in matches_ids:
        pprint(match_id)

        request_success = False
        tries = 0

        while tries < 10:
            response = requests.get(
                url,
                params={"match_id": match_id},
                timeout=60,
            )

            if response.status_code == 429:
                tries += 1
                print(f"Rate limited on match {match_id}. Retry {tries}/10")
                time.sleep(5)
                continue

            response.raise_for_status()
            request_success = True
            break

        if not request_success:
            print(f"Giving up on match {match_id}.")
            continue

        data = response.json()
        game = data["data"]["segments"][0]

        if not game["rounds"]:
            print(f"Empty game {match_id}, ignoring it.")
            continue

        map_name = game["map"]
        team1_tag = game["teams"]["team1"]["tag"]
        team2_tag = game["teams"]["team2"]["tag"]

        for round_json in game["rounds"]:
            round_atk_team = round_json["attacking_side"]
            round_def_team = "team2" if round_atk_team == "team1" else "team1"
            round_winner = round_json["winner"]
            round_economy = Round.compute_economy(round_json)
            round_team1score = round_json["score"]["team1"]
            round_team2score = round_json["score"]["team2"]

            round_data = Round(
                map_name,
                round_atk_team,
                round_def_team,
                round_winner,
                round_economy,
                round_team1score,
                round_team2score,
                team1_tag,
                team2_tag
            )

            round_data.to_csv("rounds.csv")

        print(f"Match {match_id} processed successfully.")


def retrieve_rounds():
    vct_events = get_all_events()
    vct_matches = get_all_matches_ids_from_events(vct_events)
    get_all_rounds_from_matches(vct_matches)
