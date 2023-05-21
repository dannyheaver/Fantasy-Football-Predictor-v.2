"""
Transform the current seasons data so that it is aligned with the finished seasons' data.
"""
import json
import pandas as pd
from project.transform.individual import gameweeks_2022_23
from project.models.gameweeks import Gameweeks

parameters = json.load(open("../../project/parameters.json"))
CURRENT_SEASON = parameters["CURRENT_SEASON"]

gameweeks = Gameweeks(gameweeks_2022_23)

gameweeks.add_season(CURRENT_SEASON)
gameweeks.add_value_delta()

game_odds = pd.read_csv("../../data/game_odds/{}-game-odds.csv".format(CURRENT_SEASON))

gameweeks.map_opponent_team(game_odds)
gameweeks.add_teams()
gameweeks.add_times_of_match()

gameweeks.join_odds(game_odds)
gameweeks.add_win_expectation()

gameweeks.add_won()
gameweeks.add_total_points_range()

print("Rolling Mean Metrics:")
gameweeks.rolling_mean_metrics()
print("Shifting Match Info:")
gameweeks.shift_match_info()

gameweeks.take_useful_columns()
gameweeks.gameweeks.to_csv("../../data/clean_gameweeks/{}-clean-gameweeks.csv".format(CURRENT_SEASON), index=False)
