"""
Class to transform the gameweeks data.
"""
import pandas as pd


class Gameweeks:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.gameweeks = dataframe

    def add_season(self, season):
        """
        adds the season of the gameweek data as a column
        :return: None
        """
        self.gameweeks["season"] = season

    def align_player_names(self):
        """
        cleans the players names to align them with the end of season data
        :return: None
        """
        player_names = self.gameweeks["name"]
        split_player_names = [string.split(sep="_") for string in player_names]
        self.gameweeks["name"] = [name[0].capitalize() + " " + name[1].capitalize() for name in split_player_names]
