"""
Concatenate all the seasons gameweeks data into one master dataset.
"""
import pandas as pd
import glob
from project.models.all_seasons import AllSeasons

all_seasons = pd.concat(
    map(lambda x: pd.read_csv(x, low_memory=False), glob.glob("../../data/clean_gameweeks/*.csv")))
all_seasons = AllSeasons(all_seasons)

all_seasons.map_defender_position()
all_seasons.map_midfielder_position()

all_seasons.form_against_shift_opponent()

all_seasons.take_useful_columns()
all_seasons.all_seasons.to_csv('../../data/all_seasons.csv', index=False)
