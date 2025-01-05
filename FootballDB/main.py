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
    df.dropna(subset=['Team'], inplace=True)
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
        
        ##################################################################################
        #
        #                                   ROSTERS
        #
        #################################################################################
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
    
        ##################################################################################
        #
        #                                   TEAM STATS
        #
        #################################################################################
        (df_offense_overall,        df_offense_passing, df_offense_rushing, df_offense_kickoff_returns, 
        df_offense_punt_returns,    df_offense_punting, df_offense_scoring, df_offense_downs,
        df_defense_overall,         df_defense_passing, df_defense_rushing, df_defense_kickoff_returns, 
        df_defense_punt_returns,    df_defense_punting, df_defense_scoring, df_defense_downs) = PullTeamStats.PullTeamStats_FootballDB(year)
    
        #TODO: Update the line below to work for the team stats
        #Be sure to make the team id the index
        dataframes = {
        'df_offense_overall': [df_offense_overall, 'offense_overall'],
        'df_offense_passing': [df_offense_passing, 'offense_passing'],
        'df_offense_rushing': [df_offense_rushing, 'offense_rushing'],
        'df_offense_kickoff_returns': [df_offense_kickoff_returns, 'offense_kickoff_returns'],
        'df_offense_punt_returns': [df_offense_punt_returns, 'offense_punt_returns'],
        'df_offense_punting': [df_offense_punting, 'offense_punting'],
        'df_offense_scoring': [df_offense_scoring, 'offense_scoring'],
        'df_offense_downs': [df_offense_downs, 'offense_downs'],
        'df_defense_overall': [df_defense_overall, 'defense_overall'],
        'df_defense_passing': [df_defense_passing, 'defense_passing'],
        'df_defense_rushing': [df_defense_rushing, 'defense_rushing'],
        'df_defense_kickoff_returns': [df_defense_kickoff_returns, 'defense_kickoff_returns'],
        'df_defense_punt_returns': [df_defense_punt_returns, 'defense_punt_returns'],
        'df_defense_punting': [df_defense_punting, 'defense_punting'],
        'df_defense_scoring': [df_defense_scoring, 'defense_scoring'],
        'df_defense_downs': [df_defense_downs, 'defense_downs']}
        
        for key,value in dataframes.items():
            insert_team_stats(value[0], value[1], db_teamid_dict, db_name)
    
        ##################################################################################
        #
        #                                   PLAYER STATS
        #
        #################################################################################
        #TODO: Try this
        for player, player_url in player_dict_final.items():
            #for link in player_url:
            #start = time.time()
            df_receiving, df_fumble, df_passing, df_rushing = PullPlayerStats.PullPlayerStats_FootballDB(player, player_url, year)
            #end = time.time()
            #print(rf'{player} done. Took: {end - start} seconds')
            
            try:
                if df_receiving == None:
                    df_receiving = pd.DataFrame()
            except:
                df_receiving.reset_index(inplace=True)
                df_receiving.rename(columns={'index': 'Week'}, inplace=True)  # Rename the old index column
                df_receiving['Player'] = player
                df_receiving.set_index('Player', inplace=True)
            
            try:
                if df_fumble == None:
                    df_fumble = pd.DataFrame()
            except:
                df_fumble.reset_index(inplace=True)
                df_fumble.rename(columns={'index': 'Week'}, inplace=True)  # Rename the old index column
                df_fumble['Player'] = player
                df_fumble.set_index('Player', inplace=True)
            
            try:
                if df_passing == None:
                    df_passing = pd.DataFrame()
            except:
                df_passing.reset_index(inplace=True)
                df_passing.rename(columns={'index': 'Week'}, inplace=True)  # Rename the old index column
                df_passing['Player'] = player
                df_passing.set_index('Player', inplace=True)
            
            try:
                if df_rushing == None:
                    df_rushing = pd.DataFrame()
            except:
                df_rushing.reset_index(inplace=True)
                df_rushing.rename(columns={'index': 'Week'}, inplace=True)  # Rename the old index column
                df_rushing['Player'] = player
                df_rushing.set_index('Player', inplace=True)

                
            if df_receiving.empty:
                    pass
            else:
                try:
                    df_receiving_final = pd.concat([df_receiving, df_receiving_final])
                except:
                    df_receiving_final = df_receiving
        
            if df_fumble.empty:
                    pass
            else:
                try:
                    df_fumble_final = pd.concat([df_fumble, df_fumble_final])
                except:
                    df_fumble_final = df_fumble
        
        
            if df_passing.empty:
                    pass
            else:
                try:
                    df_passing_final = pd.concat([df_passing, df_passing_final])
                except:
                    df_passing_final = df_passing
        
        
            if df_rushing.empty:
                    pass
            else:
                try:
                    df_rushing_final = pd.concat([df_rushing, df_rushing_final])
                except:
                    df_rushing_final = df_rushing
                
            print(rf'{player} done')

        all_list = df_receiving_final.index.to_list() + df_fumble_final.index.to_list() + df_passing_final.index.to_list() +df_rushing_final.index.to_list()
        all_list = list(set(all_list))
        
        #all_df = pd.concat([df_receiving_final, df_fumble_final, df_passing_final, df_rushing_final])
        

        db_playerid_dict = {}
        for value in all_list:
            db_playerid_dict[value] = Database.get_player_id(db_name,value)
            
        dataframes = {
        'passing_df': [df_passing_final, 'passing'], 'rushing_df': [df_rushing_final, 'rushing'], 'receiving_df': [df_receiving_final, 'receiving'],
        'fumble_df': [df_fumble_final, 'fumble']}
        
        for key,value in dataframes.items():
            insert_player_stats(value[0], value[1], db_playerid_dict, db_name)
            
    print('done')