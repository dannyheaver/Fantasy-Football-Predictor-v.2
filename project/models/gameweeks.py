"""
Class to transform the gameweeks data.
"""


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
