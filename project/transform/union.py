"""
Concatenate all the seasons gameweeks data into one master dataset.
"""
import pandas as pd
import glob
from project.models.all_seasons import AllSeasons

all_gameweeks = pd.concat(
    map(lambda x: pd.read_csv(x, low_memory=False), glob.glob("../../data/clean_gameweeks/*.csv")))
gameweeks = AllSeasons(all_gameweeks)

gameweeks.map_defender_position()
gameweeks.map_midfielder_position()
gameweeks.rolling_mean_metrics()
