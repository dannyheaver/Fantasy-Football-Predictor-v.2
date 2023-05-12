"""
Individual transformations to clean the raw seasons gameweeks data.
"""


def s2018_align_player_name(player_name):
    return player_name.replace('Caglar', 'Çaglar')


def s2020_align_team_names(team_name):
    replace_dict = {
        "Utd": "United",
        "Spurs": "Tottenham"
    }
    return team_name.replace(replace_dict)


def swap_opponent_index(index):
    replace_dict = {
        8: 9,
        9: 8
    }
    return index.replace(replace_dict)
