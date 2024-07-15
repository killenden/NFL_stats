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

def insert_player_stats(df, table_name, dict, db_name):
    df['Player'] = df['Player'].map(dict)
    dtypes = Database.datatypes(df)
    Database.add_database_information(table_name,db_name,df,dtypes)

def insert_team_stats(df, table_name, dict, db_name):
    df['Team'] = df.index.map(dict)
    df = df.reset_index(drop=True) 
    dtypes = Database.datatypes(df)
    Database.add_database_information(table_name,db_name,df,dtypes)


if __name__ == '__main__':
    
    import PullRosters
    import utils
    import Database
    #db_name = r'NFL_stats\database\2023_database.db'
    for year in range(2023, 2021, -1): 
        db_name = rf'database\{year}_database.db' 
        
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
    if '2024' in db_name: 
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
            if check_csv_file(filename+'.csv') == True:
                current_dir = os.getcwd()  # Get current working directory
                file_path = os.path.join(current_dir, filename+'.csv')  # Create file path
            database_df_final = pd.read_csv(file_path)
        
        db_posid_dict = {}
        for value in database_df_final['Pos'].unique():
            db_posid_dict[value] = Database.get_pos_id(db_name,value)
        database_df_final['Pos'] = database_df_final['Pos'].map(db_posid_dict) 
        dtypes = Database.datatypes(database_df_final)
        Database.add_database_information('players',db_name,database_df_final,dtypes)
    else:
        database_df_final = pd.DataFrame()
        # for team in CBS_URLs:
        #     database_df = PullRosters.PullTeam_CBS('https://www.cbssports.com/nfl/teams/'+team+'/roster/',team)
        #     print(team)
        #     database_df_final = pd.concat([database_df_final,database_df]).reset_index(drop=True)+
        start = db_name.find('\\') + len('\\')
        end = db_name.find('_')
        year = db_name[start:end]
        database_df_final = PullRosters.PullTeam_ProFootballArchives('https://www.profootballarchives.com/'+year+'.html')
        
        
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
    
    
    import PullStats
    week_list, lk_table_mascot, lk_table, CBS_URLs, NFL_URLs = utils.init()
    standings_df = PullStats.standings(lk_table)
    
    (passing_df, rushing_df, receiving_df, int_df, fg_df, ko_df, kor_df, punt_df, puntr_df, fum_df) = PullStats.NFL_stats(lk_table_mascot, year)
            
    all_df = pd.concat([passing_df, rushing_df, receiving_df, int_df, fg_df, ko_df, kor_df, punt_df, puntr_df, fum_df]).reset_index(drop=True)
    
    db_playerid_dict = {}
    for value in all_df['Player'].unique():
        db_playerid_dict[value] = Database.get_player_id(db_name,value)
        
    dataframes = {
    'passing_df': [passing_df, 'passing'], 'rushing_df': [rushing_df, 'rushing'], 'receiving_df': [receiving_df, 'receiving'],
    'int_df': [int_df, 'interception'], 'fg_df': [fg_df, 'field_goal'], 'ko_df': [ko_df, 'kickoff'],
    'kor_df': [kor_df, 'kickoff_return'], 'punt_df': [punt_df, 'punt'], 'puntr_df': [puntr_df, 'punt_return'], 'fum_df': [fum_df, 'fumbles']}
    
    for key,value in dataframes.items():
        insert_player_stats(value[0], value[1], db_playerid_dict, db_name)
    
    (passing_off_df, rushing_off_df, receiving_off_df, scoring_off_df, downs_off_df) = PullStats.NFL_stats_off(lk_table_mascot, year)
    (passing_def_df, rushing_def_df, receiving_def_df, scoring_def_df, tackles_def_df, downs_def_df, fumbles_def_df, interception_def_df) = PullStats.NFL_stats_def(lk_table_mascot, year)
    (special_fg_df, special_scoring_df, special_kickoff_df, special_kickoff_return_df, special_punting_df, special_punting_returns_df) = PullStats.NFL_stats_st(lk_table_mascot, year)
    
    db_teamid_dict = {}
    for value in passing_off_df.index.to_list():
        db_teamid_dict[value] = Database.get_team_id_shortname(db_name,value)
    
    dataframes = {
    "passing_off_df": [passing_off_df, 'team_passing_off'], "rushing_off_df": [rushing_off_df, 'team_rushing_off'], "receiving_off_df": [receiving_off_df, 'team_receiving_off'], "scoring_off_df": [scoring_off_df, 'team_scoring_off'],"downs_off_df": [downs_off_df, 'team_downs_off'],
    "passing_def_df": [passing_def_df, 'team_passing_def'], "rushing_def_df": [rushing_def_df, 'team_rushing_def'], "receiving_def_df": [receiving_def_df, 'team_receiving_def'], "scoring_def_df": [scoring_def_df, 'team_scoring_def'], "tackles_def_df": [tackles_def_df, 'team_tackles_def'], 
    "downs_def_df": [downs_def_df, 'team_downs_def'], "fumbles_def_df": [fumbles_def_df, 'team_fumbles_def'], "interception_def_df": [interception_def_df, 'team_ints_def'],
    "special_fg_df": [special_fg_df, 'team_fg_st'], "special_scoring_df": [special_scoring_df, 'team_scoring_st'], "special_kickoff_df": [special_kickoff_df, "team_kickoff_st"], "special_kickoff_return_df": [special_kickoff_return_df, "team_kick_return_st"],
    "special_punting_df": [special_punting_df, "team_punt_st"], "special_punt_return_df": [special_punting_returns_df, "team_punt_return_st"]}
        
    for key,value in dataframes.items():
        insert_team_stats(value[0], value[1], db_teamid_dict, db_name)
        
    print('Script has completed')
        
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




