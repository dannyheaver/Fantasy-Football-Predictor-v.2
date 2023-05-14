"""
Class to transform the unioned gameweeks data.
"""


class AllSeasons:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.all_seasons = dataframe
