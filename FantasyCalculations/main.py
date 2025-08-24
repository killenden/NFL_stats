from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Database
import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Sleeper')))
import SleeperInfo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FootballDB')))
import PullPlayerStats
import PullRosters
import PullTeamStats
import CreateDatabase
import PullFromDatabase

# Fantasy Football Scoring Settings

# Passing Stats
PASS_YARDS_PER_POINT = 25   # 1 point per 25 passing yards
PASS_TD_POINTS = 4          # 4 points per passing touchdown
INT_POINTS = -2             # -2 points per interception

# Rushing Stats
RUSH_YARDS_PER_POINT = 10   # 1 point per 10 rushing yards
RUSH_TD_POINTS = 6          # 6 points per rushing touchdown

# Receiving Stats
REC_YARDS_PER_POINT = 10    # 1 point per 10 receiving yards
REC_TD_POINTS = 6           # 6 points per receiving touchdown
RECEPTION_POINTS = 1        # 1 point per reception (PPR format)

# Miscellaneous
FUMBLE_LOST_POINTS = -2     # -2 points per fumble lost
TWO_POINT_CONVERSION = 2    # 2 points per two-point conversion
FG_0_39_POINTS = 3         # 3 points per field goal (0-39 yards)
FG_40_49_POINTS = 4        # 4 points per field goal (40-49 yards)
FG_50_PLUS_POINTS = 5       # 5 points per field goal (50+ yards)
PAT_POINTS = 1              # 1 point per extra point made
DEF_SACK_POINTS = 1         # 1 point per sack
DEF_INT_POINTS = 2          # 2 points per interception
DEF_FUMBLE_REC_POINTS = 2   # 2 points per fumble recovery
DEF_SAFETY_POINTS = 2       # 2 points per safety
DEF_TD_POINTS = 6           # 6 points per defensive/special teams touchdown
DEF_SHUTOUT_POINTS = 10     # 10 points for 0 points allowed
DEF_UNDER_7_POINTS = 7      # 7 points for under 7 points allowed
DEF_UNDER_14_POINTS = 4     # 4 points for under 14 points allowed


def main(db_name, weeks, year):
    ff_points_df = PullFromDatabase.ff_points(db_name)
    ff_points_df['FF_Points'] = ff_points_df['Pass TD']*PASS_TD_POINTS
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Pass Yds']/PASS_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Pass Int']*INT_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Fum']*FUMBLE_LOST_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rush Yds']/RUSH_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rush TD']*RUSH_TD_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec']*RECEPTION_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec Yds']/REC_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec TD']/REC_TD_POINTS)
    return ff_points_df

if __name__ == '__main__':
    
    # nfl_state = SleeperInfo.get_nfl_state()
    # if nfl_state['season_type'] != 'post':
    #     year = nfl_state['season']
    #     weeks = nfl_state['week']
    # else:
    #     year = 2024
    #     weeks = 18
        
    year = 2024
    weeks = 18

    db_name = rf'database\{year}.db'

    current_directory = os.getcwd()
    
    df = main(db_name, weeks, year)
    
            
    print('done')