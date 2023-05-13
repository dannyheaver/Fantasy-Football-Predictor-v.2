"""
Transform the gameweeks data of the finished seasons so that it is aligned across seasons.
"""
import pandas as pd
from project.models.individual import gameweeks_2018_19, gameweeks_2020_21, gameweeks_2021_22

gameweeks = {
    "2016-17": pd.read_csv('../../data/gameweeks/2016-17-gameweeks.csv', encoding="latin-1"),
    "2017-18": pd.read_csv('../../data/gameweeks/2017-18-gameweeks.csv', encoding="latin-1"),
    "2018-19": gameweeks_2018_19,
    "2019-20": pd.read_csv('../../data/gameweeks/2019-20-gameweeks.csv', encoding="utf-8"),
    "2020-21": gameweeks_2020_21,
    "2021-22": gameweeks_2021_22
}
