"""
Individual transformations to clean the raw seasons gameweeks data.
"""
import pandas as pd

# The name of a player in the gameweeks data does not align with the end of season data.
gameweeks_2018_19 = pd.read_csv("../../data/gameweeks/2018-19-gameweeks.csv", encoding="latin-1")
gameweeks_2018_19["name"] = gameweeks_2018_19["name"].str.replace("Caglar", "Çaglar")

# Some team names in the 2020-21 season do not align with the previous season or the game odds.
team_name_dict = {
    "Man Utd": "Man United",
    "Sheffield Utd": "Sheffield United",
    "Spurs": "Tottenham"
}
# The opponent number for 2 teams need to be swapped to align with the game odds sorted team names.
opponent_index_dict = {
    8: 9,
    9: 8
}

gameweeks_2020_21 = pd.read_csv("../../data/gameweeks/2020-21-gameweeks.csv", encoding="utf-8")
gameweeks_2020_21["plays_for"] = gameweeks_2020_21["team"].replace(team_name_dict)
gameweeks_2020_21["opponent_team"] = gameweeks_2020_21["opponent_team"].replace(opponent_index_dict)

gameweeks_2021_22 = pd.read_csv("../../data/gameweeks/2021-22-gameweeks.csv", encoding="utf-8")
gameweeks_2021_22["opponent_team"] = gameweeks_2021_22["opponent_team"].replace(opponent_index_dict)

gameweeks_2022_23 = pd.read_csv("../../data/gameweeks/2022-23-gameweeks.csv", encoding="utf-8")
gameweeks_2022_23["opponent_team"] = gameweeks_2022_23["opponent_team"].replace(opponent_index_dict)
