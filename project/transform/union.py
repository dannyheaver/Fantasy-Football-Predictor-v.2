"""
Concatenate all the seasons gameweeks data into one master dataset.
"""
import pandas as pd
import glob
from project.models.all_seasons import AllSeasons

# all_gameweeks = pd.concat(
#     map(lambda x: pd.read_csv(x, low_memory=False), glob.glob("../../data/clean_gameweeks/*.csv")))
all_gameweeks = pd.read_csv("../../data/all_seasons.csv")
gameweeks = AllSeasons(all_gameweeks)

# gameweeks.map_defender_position()
# gameweeks.map_midfielder_position()

# print("Calculating rolling means:")
# gameweeks.rolling_mean_metrics()
# gameweeks.all_seasons.to_csv('../../data/all_seasons.csv', index=False)

print("Shifting match info:")
gameweeks.shift_match_info()
gameweeks.all_seasons.to_csv('../../data/all_seasons.csv', index=False)

print("Calculating the form against the next opponent:")
gameweeks.form_against_next_opponent()
gameweeks.all_seasons.to_csv('../../data/all_seasons.csv', index=False)

gameweeks.take_useful_columns()
gameweeks.all_seasons.to_csv('../../data/all_seasons.csv', index=False)
