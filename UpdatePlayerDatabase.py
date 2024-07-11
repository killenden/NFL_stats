from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import csv
import sqlite3

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
    week_list, lk_table_mascot, lk_table, CBS_URLs, NFL_URLs = utils.init()

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
            try:
                os.remove(file_path)
            except:
                pass
        database_df_final = pd.DataFrame()
        # for team in CBS_URLs:
        #     database_df = PullRosters.PullTeam_CBS('https://www.cbssports.com/nfl/teams/'+team+'/roster/',team)
        #     print(team)
        #     database_df_final = pd.concat([database_df_final,database_df]).reset_index(drop=True)
        for team in NFL_URLs: 
            database_df = PullRosters.PullTeam_NFL('https://www.nfl.com/teams/'+team+'/roster',team) #https://www.nfl.com/teams/buffalo-bills/roster
            print(team)
            database_df_final = pd.concat([database_df_final,database_df]).reset_index(drop=True)
        
        
        db_teamid_dict = {}
        for value in database_df_final['Team'].unique():
            value = utils.capitalize_first_character(value)
            value = utils.capitalize_after_space(value)
            db_teamid_dict[value] = Database.get_team_id(db_name,value)
            
        database_df_final['Team'] = database_df_final['Team'].map(db_teamid_dict)
        
        database_df_final['player_id'] = None
        database_df_final['player_id'] = database_df_final.index + 1
        
        database_df_final = database_df_final[database_df_final['Player'].notna() & (database_df_final['Player'] != '')]
        
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, filename)  # Create file path
        database_df_final.to_csv(file_path+'.csv', index=False)
    else:
        database_df_final = pd.read_csv(filename+'.csv')
    
            
    Database.add_database_information('players',db_name,database_df_final)
    
    
    import PullStats
    week_list, lk_table_mascot, lk_table, CBS_URLs, NFL_URLs = utils.init()
    standings_df = PullStats.standings(lk_table)
    
    (qb_df, rb_df, rec_df) = PullStats.NFL_stats(lk_table_mascot)
            
    all_df = pd.concat([qb_df,rb_df,rec_df]).reset_index(drop=True)
    
    db_playerid_dict = {}
    for value in all_df['Player'].unique():
        db_playerid_dict[value] = Database.get_player_id(db_name,value)
    
    qb_df['Player'] = qb_df['Player'].map(db_playerid_dict)    
    rb_df['Player'] = rb_df['Player'].map(db_playerid_dict)
    rec_df['Player'] = rec_df['Player'].map(db_playerid_dict)
    
    
    Database.add_database_information('passing',db_name,qb_df)
    Database.add_database_information('rushing',db_name,rb_df)
    Database.add_database_information('receiving',db_name,rec_df)
    
    
'''
SELECT players.Player, players.POS, teams.team_name
FROM players
INNER JOIN teams ON players.Team = teams.team_id
WHERE teams.shortname = 'DET';

SELECT players.Player, passing.TD, teams.team_name
FROM players
INNER JOIN teams ON players.Team = teams.team_id
INNER JOIN passing ON players.player_id = passing.Player
ORDER BY passing.TD DESC;

SELECT players.Player, rushing.TD, teams.team_name
FROM players
INNER JOIN teams ON players.Team = teams.team_id
INNER JOIN rushing ON players.player_id = rushing.Player
ORDER BY rushing.TD DESC;
'''




