from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import PullPlayerStats
import PullRosters
import PullTeamStats
import sys
import CreateDatabase
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import stats.FootballDB.Database as Database
import stats.utils as utils


if __name__ == '__main__':
    
    year = 2024
    weeks = 18

    db_name = rf'database\{year}.db'
    
    ff_points(db_name)
    
    # Assume replacements are defined somewhere (replace with actual values)
    qbReplacements = 12
    rbReplacements = 24
    wrReplacements = 24
    teReplacements = 12

    # Filter by source name
    projections_robust_avg = projections[projections["sourceName"] == "averageRobust"]

    # Calculate Value of Replacement by position
    def get_value_of_replacement(df, position, replacement_rank):
        pos_df = df[df["pos"] == position]
        relevant_points = pos_df[pos_df["positionRank"].isin([replacement_rank-1, replacement_rank, replacement_rank+1])]["points"]
        return relevant_points.mean()
                
    print('done')