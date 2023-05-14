"""
Class to transform the unioned gameweeks data.
"""
import numpy as np


class AllSeasons:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.all_seasons = dataframe

    def map_defender_position(self):
        """
        maps the defenders into either attacking defender, i.e. full back, or defensive defender, i.e. central defender
        important to note this isn't completely accurate in mapping the defenders position
        :return: None
        """
        defenders_creativity = self.all_seasons[(self.all_seasons["position"] == "DEF")].groupby(
            ["name"]).median(numeric_only=True).reset_index()
        defenders_creativity["type_of_def"] = ["AttDEF" if creativity > 2 else "DefDEF" for creativity in
                                               defenders_creativity["creativity"]]
        gameweeks = self.all_seasons.merge(defenders_creativity[["name", "type_of_def"]], on="name", how="left")
        self.all_seasons["position"] = np.where(gameweeks["position"] == "DEF", gameweeks["type_of_def"],
                                                gameweeks["position"])

    def map_midfielder_position(self):
        """
        maps the midfielders into either attacking midfielder, i.e. 10's or wingers, or defensive midfielder
        important to note this isn't completely accurate in mapping the defenders position
        :return: None
        """
        defenders_creativity = self.all_seasons[(self.all_seasons["position"] == "MID")].groupby(
            ["name"]).median(numeric_only=True).reset_index()
        defenders_creativity["type_of_mid"] = ["AttMID" if creativity > 2 else "DefMID" for creativity in
                                               defenders_creativity["threat"]]
        gameweeks = self.all_seasons.merge(defenders_creativity[["name", "type_of_mid"]], on="name",
                                           how="left")
        self.all_seasons["position"] = np.where(gameweeks["position"] == "MID", gameweeks["type_of_mid"],
                                                gameweeks["position"])
