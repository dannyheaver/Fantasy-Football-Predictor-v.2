"""
Prepare the all complete rows of the master data to train the model.
"""
import pandas as pd

all_seasons = pd.read_csv("../../data/all_seasons.csv", low_memory=False)

training_data = all_seasons[all_seasons["shift_opponent"].notna()]
