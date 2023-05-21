"""
Class to transform the gameweeks data.
"""
import pandas as pd
from tqdm import tqdm


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

    def add_value_delta(self):
        """
        calculates the delta of the players value
        :return: None
        """
        value_deltas = []
        for player in self.gameweeks["name"].unique():
            players_df = self.gameweeks[self.gameweeks["name"] == player]
            value_deltas.append(players_df["value"].diff())
        self.gameweeks["value_delta"] = pd.concat(value_deltas).sort_index()
        self.gameweeks["value_delta"] = self.gameweeks["value_delta"].fillna(0)

    def align_player_names(self):
        """
        cleans the players names to align them with the end of season data
        :return: None
        """
        player_names = self.gameweeks["name"]
        split_player_names = [string.split(sep="_") for string in player_names]
        self.gameweeks["name"] = [name[0].capitalize() + " " + name[1].capitalize() for name in split_player_names]

    def join_position(self, end_of_season):
        """
        joins the player position from the end of season data to the gameweeks data
        :param end_of_season: CleanEndOfSeason
        :return: None
        """
        self.gameweeks = self.gameweeks.merge(end_of_season.end_of_season[["name", "position"]], on="name", how="left")

    def map_opponent_team(self, game_odds):
        """
        maps the opponent team in the gameweeks data from an integer representing the teams position alphabetically in
        the league using the team names in the game odds' data
        :param game_odds: pandas.core.frame.DataFrame
        :return: None
        """
        sorted_team_names = enumerate(sorted(game_odds["HomeTeam"].unique()))
        team_name_dict = {key + 1: value for key, value in sorted_team_names}
        self.gameweeks["opponent_team"] = self.gameweeks["opponent_team"].replace(team_name_dict)

    def add_teams(self):
        """
        using the distinct opponent teams in a fixture, we add the team the player plays for where the value is the
        fixture team not equal to the opponent team
        also, adds the home and away team, where the home team is the plays for team if the player was at home, and
        the opponent team if not
        :return: None
        """
        fixture_ids = {}
        for i in range(1, max(self.gameweeks["fixture"] + 1)):
            fixture_ids[i] = set(self.gameweeks[self.gameweeks["fixture"] == i]["opponent_team"])

        zipped_team_info = zip(self.gameweeks["was_home"], self.gameweeks["opponent_team"], self.gameweeks["fixture"])
        plays_for, home_teams, away_teams = [], [], []
        for was_home, opponent_team, fixture in zipped_team_info:
            team_plays_for = [team for team in fixture_ids[fixture] if team != opponent_team][0]
            plays_for.append(team_plays_for)
            if was_home:
                home_teams.append(team_plays_for)
                away_teams.append(opponent_team)
            else:
                home_teams.append(opponent_team)
                away_teams.append(team_plays_for)

        self.gameweeks["plays_for"] = plays_for
        self.gameweeks["HomeTeam"] = home_teams
        self.gameweeks["AwayTeam"] = away_teams

    def add_times_of_match(self):
        """
        convert the kickoff time to BST and then extract the date, month and time of the match
        :return: None
        """
        self.gameweeks["kickoff_time"] = pd.to_datetime(self.gameweeks["kickoff_time"], utc=True).dt.tz_convert(
            "Europe/London")
        self.gameweeks["date_of_match"] = self.gameweeks["kickoff_time"].dt.date
        self.gameweeks["month_of_match"] = self.gameweeks["kickoff_time"].dt.month
        self.gameweeks["time_of_match"] = self.gameweeks["kickoff_time"].dt.strftime("%H:%M")

    def join_odds(self, game_odds):
        """
        joins the BET365 home and away team odds to win the match from the game odds data to the gameweeks data
        :param game_odds: pandas.core.frame.DataFrame
        :return: None
        """
        self.gameweeks = self.gameweeks.merge(game_odds[["HomeTeam", "AwayTeam", "B365H", "B365A", "FTR"]],
                                              on=["HomeTeam", "AwayTeam"], how="left")

    def add_win_expectation(self):
        """
        adds the win expectation of the players team from the BET365 odds
        :return: None
        """
        zipped_bet_odds = zip(self.gameweeks["was_home"], self.gameweeks["B365H"], self.gameweeks["B365A"])
        self.gameweeks["win_expectation"] = [B365A / B365H if was_home else B365H / B365A for was_home, B365H, B365A in
                                             zipped_bet_odds]

    def add_won(self):
        """
        adds a boolean column that's true if the players team won the match
        :return: None
        """
        home_or_away = ["H" if was_home else "A" for was_home in self.gameweeks["was_home"]]
        zipped_results = zip(home_or_away, self.gameweeks["FTR"])
        self.gameweeks["is_won"] = [0 if ftr == "D" else 1 if home_or_away == ftr else -1 for home_or_away, ftr in
                                    zipped_results]

    def add_total_points_range(self):
        """
        groups the players total points into points cohorts
        :return: None
        """
        total_points = self.gameweeks["total_points"]
        self.gameweeks["total_points_range"] = pd.cut(total_points, [total_points.min()-1, 0, 1, 4, 10,
                                                                     total_points.max()+1], labels=[0, 1, 2, 3, 4])
    
    def rolling_mean_metrics(self):
        """
        takes the players 3 matches prior to the gameweek and means their metrics for a representation of their form
        :return: None
        """
        mean_points, mean_minutes, mean_creativity, mean_threat, mean_influence, mean_bps, mean_goals, mean_assists, \
            mean_conceded = ([] for _ in range(9))
        zipped_names = zip(self.gameweeks["name"], self.gameweeks["date_of_match"])
        for player, date in tqdm(list(zipped_names)):
            players_df = self.gameweeks[
                             (self.gameweeks["name"] == player) & (self.gameweeks["date_of_match"] < date)][
                         :3]
            mean_points.append(players_df["total_points"].mean())
            mean_minutes.append(players_df["minutes"].mean())
            mean_creativity.append(players_df["creativity"].mean())
            mean_threat.append(players_df["threat"].mean())
            mean_influence.append(players_df["influence"].mean())
            mean_bps.append(players_df["bps"].mean())
            mean_goals.append(players_df["goals_scored"].mean())
            mean_assists.append(players_df["assists"].mean())
            mean_conceded.append(players_df["goals_conceded"].mean())
        self.gameweeks["mean_total_points"] = mean_points
        self.gameweeks["mean_minutes"] = mean_minutes
        self.gameweeks["mean_creativity"] = mean_creativity
        self.gameweeks["mean_threat"] = mean_threat
        self.gameweeks["mean_influence"] = mean_influence
        self.gameweeks["mean_bps"] = mean_bps
        self.gameweeks["mean_goals"] = mean_goals
        self.gameweeks["mean_assists"] = mean_assists
        self.gameweeks["mean_conceded"] = mean_conceded
        self.gameweeks["mean_total_points"] = self.gameweeks["mean_total_points"].fillna(
            self.gameweeks["total_points"])
        self.gameweeks["mean_minutes"] = self.gameweeks["mean_minutes"].fillna(self.gameweeks["minutes"])
        self.gameweeks["mean_creativity"] = self.gameweeks["mean_creativity"].fillna(self.gameweeks["creativity"])
        self.gameweeks["mean_threat"] = self.gameweeks["mean_threat"].fillna(self.gameweeks["threat"])
        self.gameweeks["mean_influence"] = self.gameweeks["mean_influence"].fillna(self.gameweeks["influence"])
        self.gameweeks["mean_bps"] = self.gameweeks["mean_bps"].fillna(self.gameweeks["bps"])
        self.gameweeks["mean_goals"] = self.gameweeks["mean_goals"].fillna(self.gameweeks["goals_scored"])
        self.gameweeks["mean_assists"] = self.gameweeks["mean_assists"].fillna(self.gameweeks["assists"])
        self.gameweeks["mean_conceded"] = self.gameweeks["mean_conceded"].fillna(self.gameweeks["goals_conceded"])

    def shift_match_info(self):
        """
        shift match info and key metrics for each player for their next game
        :return: None
        """
        shift_points_range, shift_value, shift_value_delta, shift_opponent, shift_we, shift_mean_minutes, shift_mom, \
            shift_tom, shift_home, shift_mean_points, shift_mean_creativity, shift_mean_threat, shift_mean_influence, \
            shift_mean_bps, shift_mean_goals, shift_mean_assists, shift_mean_conceded = ([] for _ in range(17))
        for player in tqdm(list(self.gameweeks["name"].unique())):
            players_df = self.gameweeks[self.gameweeks["name"] == player].sort_values(by="date_of_match", ascending=False)
            shift_points_range.append(players_df["total_points_range"].shift())
            shift_value.append(players_df["value"].shift())
            shift_value_delta.append(players_df["value_delta"].shift())
            shift_opponent.append(players_df["opponent_team"].shift())
            shift_we.append(players_df["win_expectation"].shift())
            shift_mom.append(players_df["month_of_match"].shift())
            shift_tom.append(players_df["time_of_match"].shift())
            shift_home.append(players_df["was_home"].shift())
            shift_mean_minutes.append(players_df["mean_minutes"].shift())
            shift_mean_points.append(players_df["mean_total_points"].shift())
            shift_mean_creativity.append(players_df["mean_creativity"].shift())
            shift_mean_threat.append(players_df["mean_threat"].shift())
            shift_mean_influence.append(players_df["mean_influence"].shift())
            shift_mean_bps.append(players_df["mean_bps"].shift())
            shift_mean_goals.append(players_df["mean_goals"].shift())
            shift_mean_assists.append(players_df["mean_assists"].shift())
            shift_mean_conceded.append(players_df["mean_conceded"].shift())
        self.gameweeks["shift_total_points_range"] = pd.concat(shift_points_range).sort_index()
        self.gameweeks["shift_value"] = pd.concat(shift_value).sort_index()
        self.gameweeks["shift_value_delta"] = pd.concat(shift_value_delta).sort_index()
        self.gameweeks["shift_opponent"] = pd.concat(shift_opponent).sort_index()
        self.gameweeks["shift_win_expectation"] = pd.concat(shift_we).sort_index()
        self.gameweeks["shift_month_of_match"] = pd.concat(shift_mom).sort_index()
        self.gameweeks["shift_time_of_match"] = pd.concat(shift_tom).sort_index()
        self.gameweeks["shift_was_home"] = pd.concat(shift_home).sort_index()
        self.gameweeks["shift_mean_minutes"] = pd.concat(shift_mean_minutes).sort_index()
        self.gameweeks["shift_mean_total_points"] = pd.concat(shift_mean_points).sort_index()
        self.gameweeks["shift_mean_creativity"] = pd.concat(shift_mean_creativity).sort_index()
        self.gameweeks["shift_mean_threat"] = pd.concat(shift_mean_threat).sort_index()
        self.gameweeks["shift_mean_influence"] = pd.concat(shift_mean_influence).sort_index()
        self.gameweeks["shift_mean_bps"] = pd.concat(shift_mean_bps).sort_index()
        self.gameweeks["shift_mean_goals"] = pd.concat(shift_mean_goals).sort_index()
        self.gameweeks["shift_mean_assists"] = pd.concat(shift_mean_assists).sort_index()
        self.gameweeks["shift_mean_conceded"] = pd.concat(shift_mean_conceded).sort_index()

    def take_useful_columns(self):
        """
        removes all depreciated columns
        :return: None
        """
        useful_columns = ["season", "name", "position", "value", "value_delta", "minutes", "total_points",
                          "total_points_range", "assists", "goals_scored", "goals_conceded", "saves", "own_goals",
                          "penalties_missed", "penalties_saved", "clean_sheets", "creativity", "threat", "influence",
                          "bps", "minutes", "yellow_cards", "red_cards", "plays_for", "opponent_team", "was_home",
                          "is_won", "month_of_match", "time_of_match", "win_expectation", "date_of_match",
                          "mean_total_points", "mean_minutes", "mean_creativity", "mean_threat", "mean_influence",
                          "mean_bps", "mean_goals", "mean_assists", "mean_conceded", "shift_total_points_range",
                          "shift_value", "shift_value_delta", "shift_opponent", "shift_win_expectation",
                          "shift_month_of_match", "shift_time_of_match", "shift_was_home", "shift_mean_minutes",
                          "shift_mean_total_points", "shift_mean_creativity", "shift_mean_threat",
                          "shift_mean_influence", "shift_mean_bps", "shift_mean_goals", "shift_mean_assists",
                          "shift_mean_conceded"]
        self.gameweeks = self.gameweeks[useful_columns]
