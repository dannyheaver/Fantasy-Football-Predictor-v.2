"""
Class to transform the end of season data.
"""


class EndOfSeason:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.end_of_season = dataframe

    def align_player_names(self):
        """
        cleans the players names to align them with the end of season data
        :return: None
        """
        zipped_player_names = zip(self.end_of_season["first_name"], self.end_of_season["second_name"])
        self.end_of_season["name"] = [name[0].capitalize() + ' ' + name[1].capitalize() for name in zipped_player_names]

    def map_position(self):
        """
        maps the element type of the player to his position as a string
        :return: None
        """
        position_dict = {
            1: "GK",
            2: "DEF",
            3: "MID",
            4: "FWD"
        }
        self.end_of_season["position"] = self.end_of_season["element_type"].replace(position_dict)
