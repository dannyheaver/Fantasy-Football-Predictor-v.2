"""
Prepare the all complete rows of the master data to train the model.
"""
import pandas as pd
from project.models.training import Training

all_seasons = pd.read_csv("../../data/all_seasons.csv", low_memory=False)

training_data = all_seasons[all_seasons["shift_opponent"].notna()]
training_data = Training(training_data)
training_data.dummify_categories()
x_train, x_test, y_train, y_test, transformer = training_data.split_into_train_and_test()
