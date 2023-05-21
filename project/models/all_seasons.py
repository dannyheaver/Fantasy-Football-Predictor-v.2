"""
Class to transform the unioned gameweeks data.
"""
import numpy as np
from tqdm import tqdm


class AllSeasons:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.all_seasons = dataframe

    def map_defender_position(self):
        """
        maps the defenders into either attacking defender, i.e. full back, or defensive defender, i.e. central defender
        important to note this isn"t completely accurate in mapping the defenders position
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
        maps the midfielders into either attacking midfielder, i.e. 10"s or wingers, or defensive midfielder
        important to note this isn"t completely accurate in mapping the defenders position
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

    def form_against_shift_opponent(self):
        """
        calculates the mean of the key metrics against the next opponent
        :return: None
        """
        points_ano, creativity_ano, threat_ano, influence_ano, bps_ano, goals_ano, assists_ano, conceded_ano = ([] for _
                                                                                                                in
                                                                                                                range(
                                                                                                                    8))
        zipped_opponent_info = zip(self.all_seasons["name"], self.all_seasons["shift_opponent"])
        for player, opponent in tqdm(list(zipped_opponent_info)):
            players_df = self.all_seasons[
                (self.all_seasons["name"] == player) & (
                    self.all_seasons["opponent_team"] == opponent)]
            points_ano.append(players_df["total_points"].mean())
            creativity_ano.append(players_df["creativity"].mean())
            threat_ano.append(players_df["threat"].mean())
            influence_ano.append(players_df["influence"].mean())
            bps_ano.append(players_df["bps"].mean())
            goals_ano.append(players_df["goals_scored"].mean())
            assists_ano.append(players_df["assists"].mean())
            conceded_ano.append(players_df["goals_conceded"].mean())
        self.all_seasons["points_against_shift_opponent"] = points_ano
        self.all_seasons["creativity_against_shift_opponent"] = creativity_ano
        self.all_seasons["threat_against_shift_opponent"] = threat_ano
        self.all_seasons["influence_against_shift_opponent"] = influence_ano
        self.all_seasons["bps_against_shift_opponent"] = bps_ano
        self.all_seasons["goals_against_shift_opponent"] = goals_ano
        self.all_seasons["assists_against_shift_opponent"] = assists_ano
        self.all_seasons["conceded_against_shift_opponent"] = conceded_ano
        self.all_seasons["points_against_shift_opponent"] = self.all_seasons["points_against_shift_opponent"].fillna(
            self.all_seasons["mean_total_points"])
        self.all_seasons["creativity_against_shift_opponent"] = self.all_seasons[
            "creativity_against_shift_opponent"].fillna(self.all_seasons["mean_creativity"])
        self.all_seasons["threat_against_shift_opponent"] = self.all_seasons["threat_against_shift_opponent"].fillna(
            self.all_seasons["mean_threat"])
        self.all_seasons["influence_against_shift_opponent"] = self.all_seasons[
            "influence_against_shift_opponent"].fillna(self.all_seasons["mean_influence"])
        self.all_seasons["bps_against_shift_opponent"] = self.all_seasons["bps_against_shift_opponent"].fillna(
            self.all_seasons["mean_bps"])
        self.all_seasons["goals_against_shift_opponent"] = self.all_seasons["goals_against_shift_opponent"].fillna(
            self.all_seasons["mean_goals"])
        self.all_seasons["assists_against_shift_opponent"] = self.all_seasons["assists_against_shift_opponent"].fillna(
            self.all_seasons["mean_assists"])
        self.all_seasons["conceded_against_shift_opponent"] = self.all_seasons[
            "conceded_against_shift_opponent"].fillna(self.all_seasons["mean_conceded"])

    def take_useful_columns(self):
        """
        removes all depreciated columns
        :return: None
        """
        useful_columns = ["season", "name", "position", "plays_for", "shift_total_points_range", "shift_value",
                          "shift_value_delta", "shift_opponent", "shift_win_expectation", "shift_month_of_match",
                          "shift_time_of_match", "shift_was_home", "shift_mean_minutes", "shift_mean_total_points",
                          "shift_mean_creativity", "shift_mean_threat", "shift_mean_influence", "shift_mean_bps",
                          "shift_mean_goals", "shift_mean_assists", "shift_mean_conceded",
                          "points_against_shift_opponent", "creativity_against_shift_opponent",
                          "threat_against_shift_opponent", "influence_against_shift_opponent",
                          "bps_against_shift_opponent", "goals_against_shift_opponent",
                          "assists_against_shift_opponent", "conceded_against_shift_opponent"]
        self.all_seasons = self.all_seasons[useful_columns]

