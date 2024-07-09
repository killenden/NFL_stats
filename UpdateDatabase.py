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
    current_dir = os.path.dirname(os.path.realpath(__file__))
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
    
    print(os.path.dirname(os.path.realpath(__file__)))
    
    reset_db = input('Do you want to init the db? (y/n)   ')
    if reset_db == 'y':
        reset_db1 = input('Are you sure? (y/n)   ')
        if reset_db1 == 'y':
            Database.create_nfl_analytics_db(db_name)
    week_list, lk_table_mascot, lk_table, NFL_URLs = utils.init()

    filename = 'temp_db'
    
    reset_csv_out = False
    reset_csv = input('Do you want to reset the csv? (y/n)   ')
    if reset_csv == 'y':
        reset_csv1 = input('Are you sure? (y/n)   ')
        if reset_csv1 == 'y':
           reset_csv_out = True
    
    if reset_csv_out or check_csv_file(filename+'.csv') == False:
        if check_csv_file(filename+'.csv') == True:
            current_dir = os.getcwd()  # Get current working directory
            file_path = os.path.join(current_dir, filename+'.csv')  # Create file path
            os.remove(file_path)
        database_df_final = pd.DataFrame()
        for team in NFL_URLs:
            database_df = PullRosters.PullTeam('https://www.cbssports.com/nfl/teams/'+team+'/roster/',team)
            print(team)
            database_df_final = pd.concat([database_df_final,database_df]).reset_index(drop=True)
        
        
        db_teamid_dict = {}
        for value in database_df_final['Team'].unique():
            db_teamid_dict[value] = Database.get_team_id(db_name,value)
            
        database_df_final['Team'] = database_df_final['Team'].map(db_teamid_dict)
        
        database_df_final['player_id'] = None
        database_df_final['player_id'] = database_df_final.index + 1
        
        database_df_final = database_df_final[database_df_final['Player'].notna() & (database_df_final['Player'] != '')]
        
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, filename)  # Create file path
        database_df_final.to_csv(file_path+'.csv', index=False)
    else:
        df = pd.read_csv(filename.endswith('.csv'))
    
    
        
    Database.add_players_info(db_name,database_df_final)
    
    
    
'''
SELECT players.Player, players.POS, teams.team_name
FROM players
INNER JOIN teams ON players.Team = teams.team_id
WHERE teams.shortname = 'DET';
'''
