"""
Transform the current seasons data so that it is aligned with the finished seasons' data.
"""
from project.models.individual import gameweeks_2022_23
from project.models.gameweeks import Gameweeks

CURRENT_SEASON = "2022-23"

gameweeks = Gameweeks(gameweeks_2022_23)

gameweeks.add_season(CURRENT_SEASON)
