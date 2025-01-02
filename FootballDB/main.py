from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import PullPlayerStats
import PullRosters
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Database
import utils
import CreateDatabase

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
    
    for year in range(2024, 2025): 
        filename, db_name = CreateDatabase.create_db(year)
                
        database_df_final = pd.DataFrame()
        
        #used for webscraping
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

        r = requests.get('https://www.footballdb.com/teams/index.html', headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        
        database_df_final, player_dict_final = PullRosters.ScrapingFootballDB(soup)
        
        db_teamid_dict = {}
        for value in database_df_final['Team'].unique():
            value = utils.capitalize_first_character(value)
            value = utils.capitalize_after_space(value)
            db_teamid_dict[value] = Database.get_team_id(db_name,value)
            
        database_df_final['Team'] = database_df_final['Team'].map(db_teamid_dict)
        
        database_df_final['player_id'] = None
        database_df_final['player_id'] = database_df_final.index + 1
        
        database_df_final = database_df_final[database_df_final['Player'].notna() & (database_df_final['Player'] != '')]

        db_posid_dict = {}
        for value in database_df_final['Pos'].unique():
            db_posid_dict[value] = Database.get_pos_id(db_name,value)
        database_df_final['Pos'] = database_df_final['Pos'].map(db_posid_dict) 
        
        
        dtypes = Database.datatypes(database_df_final)
        Database.add_database_information('players',db_name,database_df_final,dtypes)
    
        #TODO: Try this
        for player, player_url in player_dict_final.items():
            #for link in player_url:
            #start = time.time()
            df_receiving, df_fumble, df_passing, df_rushing = PullRosters.PullPlayerStats_FootballDB(player_url, year)
            #end = time.time()
            #print(rf'{player} done. Took: {end - start} seconds')
            print(rf'{player} done')

        all_df = pd.concat([df_receiving, df_fumble, df_passing, df_rushing]).reset_index(drop=True)
        

        db_playerid_dict = {}
        for value in all_df['Player'].unique():
            db_playerid_dict[value] = Database.get_player_id(db_name,value)
            
        dataframes = {
        'passing_df': [df_passing, 'passing'], 'rushing_df': [df_rushing, 'rushing'], 'receiving_df': [df_receiving, 'receiving'],
        'fumble_df': [df_fumble, 'fumble']}
        
        for key,value in dataframes.items():
            insert_player_stats(value[0], value[1], db_playerid_dict, db_name)
            
        #TODO: Grab the team stats
        # https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr=2024&type=reg&cat=S&group=O&conf=&sort=tottd
        #Relatively easy way to grab the team stats. Look at the cat and group
    print('done')