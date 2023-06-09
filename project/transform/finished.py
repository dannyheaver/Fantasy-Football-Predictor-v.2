"""
Transform the gameweeks data of the finished seasons so that it is aligned across seasons.
"""
import pandas as pd
from project.transform.individual import gameweeks_2018_19, gameweeks_2020_21, gameweeks_2021_22
from project.models.gameweeks import Gameweeks
from project.models.end_of_season import EndOfSeason

gameweeks_dict = {
    "2016-17": pd.read_csv('../../data/gameweeks/2016-17-gameweeks.csv', encoding="latin-1"),
    "2017-18": pd.read_csv('../../data/gameweeks/2017-18-gameweeks.csv', encoding="latin-1"),
    "2018-19": gameweeks_2018_19,
    "2019-20": pd.read_csv('../../data/gameweeks/2019-20-gameweeks.csv', encoding="utf-8"),
    "2020-21": gameweeks_2020_21,
    "2021-22": gameweeks_2021_22
}

for season in gameweeks_dict.keys():
    print(season)
    gameweeks = Gameweeks(gameweeks_dict[season])

    gameweeks.add_season(season)
    gameweeks.add_value_delta()

    if season in {"2016-17", "2017-18", "2018-19", "2019-20"}:
        gameweeks.align_player_names()

        end_of_season_df = pd.read_csv("../../data/end_of_season/{}-end-of-season.csv".format(season))

        end_of_season = EndOfSeason(end_of_season_df)
        end_of_season.align_player_names()
        end_of_season.map_position()

        gameweeks.join_position(end_of_season)

    game_odds = pd.read_csv("../../data/game_odds/{}-game-odds.csv".format(season))

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
    gameweeks.gameweeks.to_csv("../../data/clean_gameweeks/{}-clean-gameweeks.csv".format(season), index=False)
