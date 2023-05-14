"""
Transform the current seasons data so that it is aligned with the finished seasons' data.
"""
import pandas as pd
from project.models.individual import gameweeks_2022_23
from project.models.gameweeks import Gameweeks

CURRENT_SEASON = "2022-23"

gameweeks = Gameweeks(gameweeks_2022_23)

gameweeks.add_season(CURRENT_SEASON)

game_odds = pd.read_csv("../../data/game_odds/{}-game-odds.csv".format(CURRENT_SEASON))

gameweeks.map_opponent_team(game_odds)
gameweeks.add_teams()
gameweeks.add_times_of_match()
gameweeks.join_odds(game_odds)
gameweeks.add_win_expectation()
