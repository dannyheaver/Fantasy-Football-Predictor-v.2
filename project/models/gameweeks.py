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
