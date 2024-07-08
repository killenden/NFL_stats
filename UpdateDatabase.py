from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import csv

def check_csv_file(filename):
    """
    Check if a CSV file exists in the current directory.

    Parameters:
    - filename (str): Name of the CSV file to check.

    Returns:
    - bool: True if the CSV file exists, False otherwise.
    """
    current_dir = os.getcwd()  # Get current working directory
    file_path = os.path.join(current_dir, filename)  # Create file path

    if os.path.isfile(file_path) and filename.endswith('.csv'):
        return True
    else:
        return False


if __name__ == '__main__':
    
    import PullRosters
    import utils
    import Database
    db_name = r'NFL_stats\database\2023_database.db'
    
    Database.create_nfl_analytics_db(db_name)
    week_list, lk_table_mascot, lk_table, NFL_URLs = utils.init()

    filename = 'temp_db'
    #TODO: UPDATE THIS IF STATEMENT SO IT ACTUALLY WORKS
    if check_csv_file(filename) == False:
        database_df_final = pd.DataFrame()
        for team in NFL_URLs:
            database_df = PullRosters.PullTeam('https://www.cbssports.com/nfl/teams/'+team+'/roster/',team)
            print(team)
            database_df_final = pd.concat([database_df_final,database_df]).reset_index(drop=True)
        
        #TODO: UPDATE THIS SECTION TO PULL THE IDs
        db_teamid_dict = {}
        for value in database_df_final['Team'].unique():
            db_teamid_dict[value] = Database.get_team_id(db_name,value)
            
        database_df_final['Team'].map(db_teamid_dict)
        
        db_playerid_dict = {}
        for value in database_df_final['Player'].unique():
            db_teamid_dict[value] = Database.get_team_id(db_name,value)
                
        database_df_final['PlayerID'] = None
        
        database_df_final['PlayerID'].map(db_teamid_dict)
        
        #############
        
        current_dir = os.getcwd()  # Get current working directory
        file_path = os.path.join(current_dir, filename)  # Create file path
        database_df_final.to_csv(file_path+'.csv', index=False)
    else:
        df = pd.read_csv(filename.endswith('.csv'))
    
    
        
    Database.add_players_info(db_name,database_df_final)
