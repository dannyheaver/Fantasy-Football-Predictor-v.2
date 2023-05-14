"""
Class to transform the unioned gameweeks data.
"""
import numpy as np
import pandas as pd


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

    def rolling_mean_metrics(self):
        """
        takes the players 3 matches prior to the gameweek and means their metrics for a representation of their form
        :return: None
        """
        mean_points, mean_creativity, mean_threat, mean_influence, mean_bps, mean_goals, mean_assists, mean_conceded = (
            [] for _ in range(8))
        for player, date in zip(self.all_seasons["name"], self.all_seasons["date_of_match"]):
            players_df = self.all_seasons[(self.all_seasons["name"] == player) & (self.all_seasons["date_of_match"] < date)][
                         :3]
            mean_points.append(players_df["adjusted_points"].mean())
            mean_creativity.append(players_df["creativity"].mean())
            mean_threat.append(players_df["threat"].mean())
            mean_influence.append(players_df["influence"].mean())
            mean_bps.append(players_df["bps"].mean())
            mean_goals.append(players_df["goals_scored"].mean())
            mean_assists.append(players_df["assists"].mean())
            mean_conceded.append(players_df["goals_conceded"].mean())
        self.all_seasons["mean_adjusted_points"] = mean_points
        self.all_seasons["mean_creativity"] = mean_creativity
        self.all_seasons["mean_threat"] = mean_threat
        self.all_seasons["mean_influence"] = mean_influence
        self.all_seasons["mean_bps"] = mean_bps
        self.all_seasons["mean_goals"] = mean_goals
        self.all_seasons["mean_assists"] = mean_assists
        self.all_seasons["mean_conceded"] = mean_conceded
        self.all_seasons["mean_adjusted_points"] = self.all_seasons["mean_adjusted_points"].fillna(
            self.all_seasons["adjusted_points"])
        self.all_seasons["mean_creativity"] = self.all_seasons["mean_creativity"].fillna(self.all_seasons["creativity"])
        self.all_seasons["mean_threat"] = self.all_seasons["mean_threat"].fillna(self.all_seasons["threat"])
        self.all_seasons["mean_influence"] = self.all_seasons["mean_influence"].fillna(self.all_seasons["influence"])
        self.all_seasons["mean_bps"] = self.all_seasons["mean_bps"].fillna(self.all_seasons["bps"])
        self.all_seasons["mean_goals"] = self.all_seasons["mean_goals"].fillna(self.all_seasons["goals_scored"])
        self.all_seasons["mean_assists"] = self.all_seasons["mean_assists"].fillna(self.all_seasons["assists"])
        self.all_seasons["mean_conceded"] = self.all_seasons["mean_conceded"].fillna(self.all_seasons["goals_conceded"])

    def shift_match_info(self):
        """
        shift match info and key metrics for each player for their next game
        :return: None
        """
        shift_points, shift_value, shift_value_delta, shift_opponent, shift_we, shift_mom, shift_tom, shift_home, \
            shift_mean_points, shift_mean_creativity, shift_mean_threat, shift_mean_influence, shift_mean_bps, \
            shift_mean_goals, shift_mean_assists, shift_mean_conceded = ([] for _ in range(16))
        for player in self.all_seasons["name"].unique():
            players_df = self.all_seasons[self.all_seasons["name"] == player].sort_values(by="date_of_match",
                                                                                          ascending=False)
            shift_points.append(players_df["adjusted_points"].shift())
            shift_value.append(players_df["value"].shift())
            shift_value_delta.append(players_df["value_delta"].shift())
            shift_opponent.append(players_df["opponent_team"].shift())
            shift_we.append(players_df["win_expectation"].shift())
            shift_mom.append(players_df["month_of_match"].shift())
            shift_tom.append(players_df["time_of_match"].shift())
            shift_home.append(players_df["was_home"].shift())
            shift_mean_points.append(players_df["mean_adjusted_points"].shift())
            shift_mean_creativity.append(players_df["mean_creativity"].shift())
            shift_mean_threat.append(players_df["mean_threat"].shift())
            shift_mean_influence.append(players_df["mean_influence"].shift())
            shift_mean_bps.append(players_df["mean_bps"].shift())
            shift_mean_goals.append(players_df["mean_goals"].shift())
            shift_mean_assists.append(players_df["mean_assists"].shift())
            shift_mean_conceded.append(players_df["mean_conceded"].shift())
        self.all_seasons["shift_adjusted_points"] = pd.concat(shift_points).sort_index()
        self.all_seasons["shift_value"] = pd.concat(shift_value).sort_index()
        self.all_seasons["shift_value_delta"] = pd.concat(shift_value_delta).sort_index()
        self.all_seasons["shift_opponent"] = pd.concat(shift_opponent).sort_index()
        self.all_seasons["shift_win_expectation"] = pd.concat(shift_we).sort_index()
        self.all_seasons["shift_month_of_match"] = pd.concat(shift_mom).sort_index()
        self.all_seasons["shift_time_of_match"] = pd.concat(shift_tom).sort_index()
        self.all_seasons["shift_was_home"] = pd.concat(shift_home).sort_index()
        self.all_seasons["shift_mean_adjusted_points"] = pd.concat(shift_mean_points).sort_index()
        self.all_seasons["shift_mean_creativity"] = pd.concat(shift_mean_creativity).sort_index()
        self.all_seasons["shift_mean_threat"] = pd.concat(shift_mean_threat).sort_index()
        self.all_seasons["shift_mean_influence"] = pd.concat(shift_mean_influence).sort_index()
        self.all_seasons["shift_mean_bps"] = pd.concat(shift_mean_bps).sort_index()
        self.all_seasons["shift_mean_goals"] = pd.concat(shift_mean_goals).sort_index()
        self.all_seasons["shift_mean_assists"] = pd.concat(shift_mean_assists).sort_index()
        self.all_seasons["shift_mean_conceded"] = pd.concat(shift_mean_conceded).sort_index()
