"""
Prepare the latest gameweek data, for each player who plays for a team in the next FPL gameweek,
for predicting.
"""
import json
import pandas as pd

parameters = json.load(open("../../project/parameters.json"))
CURRENT_SEASON = parameters["CURRENT_SEASON"]

all_seasons = pd.read_csv("../../data/all_seasons.csv")

recent_gameweek = all_seasons[(all_seasons["season"] == CURRENT_SEASON) & (all_seasons["shift_opponent"].isnull())]
recent_gameweek.drop(["shift_total_points_range"], axis=1, inplace=True)
