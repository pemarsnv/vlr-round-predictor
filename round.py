import csv
from enumeration.economy import Economy
from pathlib import Path

class Round:
    def __init__(self, map_name, atk_team, def_team, winner_team, economy, team1_score, team2_score, team1_tag, team2_tag):
        self.map_name = map_name
        self.atk_team = atk_team
        self.def_team = def_team
        self.winner_team = team1_tag if winner_team == 'team1' else team2_tag
        self.economy = economy
        if 'team1' == atk_team:
            self.score_atk = team1_score
            self.score_def = team2_score
            self.atk_team = team1_tag
            self.def_team = team2_tag
        else:
            self.score_atk = team2_score
            self.score_def = team1_score
            self.atk_team = team2_tag
            self.def_team = team1_tag

    @staticmethod
    def compute_economy(round_json):
        economy = round_json['economy']
        atk_loadout = 0
        def_loadout = 0

        atk_team = int(round_json['attacking_side'][-1])
        for loadout in economy:
            if loadout['team'] == atk_team:
                atk_loadout += loadout['spent']
            else:
                def_loadout += loadout['spent']

        if atk_loadout >= def_loadout+12500:
            return Economy.DEF_THRIFTY
        elif def_loadout >= atk_loadout+12500:
            return Economy.ATK_THRIFTY
        else:
            return Economy.NORMAL

    def to_csv(self, file_path):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        row = {
            "map_name": self.map_name,
            "atk_team": self.atk_team,
            "def_team": self.def_team,
            "winner_team": self.winner_team,
            "economy": (
                self.economy.name
                if isinstance(self.economy, Economy)
                else self.economy
            ),
            "score_atk": self.score_atk,
            "score_def": self.score_def,
        }

        write_header = not path.exists() or path.stat().st_size == 0

        with path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(row))

            if write_header:
                writer.writeheader()

            writer.writerow(row)

    def describe(self):
        # Small description of the round result
        return (
            f"{self.atk_team} attacks against "
            f"{self.def_team} on {self.map_name} "
            f"{self.winner_team} wins "
            f"result: {self.economy}, {self.score_atk} - {self.score_def}"
        )