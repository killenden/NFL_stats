from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
from PullPlayerStats import *
from PullRosters import *
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database import *


if __name__ == '__main__':
    
    #used for webscraping
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    r = requests.get('https://www.footballdb.com/teams/index.html', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    footballdb_dict = {}
    roster_links = []
    for team in soup.find_all(class_ = 'teams-item teams-league-NFL'):
        for team_info in team.contents:
            try:
                if 'teams-infobox' in team_info.attrs['class'][0]:
                    for info in team_info.contents:
                        try:
                            if 'teams-teamname' in info.attrs['class'][0]:
                                team_name = info.contents[0].text
                            if 'teams-teamlinks' in info.attrs['class'][0]:
                                for link in info.contents:
                                    try:
                                        if 'roster' in link.attrs['title'].lower():
                                            footballdb_dict[team_name] = link.attrs['href']
                                        #TODO: add additional if statements here to grab the other links:
                                            #results
                                            #stats
                                            #transactions
                                    except:
                                        continue
                        except:
                            continue
            except:
                continue
    for team_name, link in footballdb_dict.items():
        df, player_dict = PullTeam_FootballDB(rf'https://www.footballdb.com{link}',team_name)
        try:
            df_final = pd.concat([df, df_final], ignore_index=True).reset_index(drop=True)
            player_dict_final.update(player_dict)
        except:
            df_final = df
            player_dict_final = player_dict
        print(rf'{team_name} complete')
        
    for player, player_url in player_dict_final.items():
        year = '2024'
        start = find_nth(player_url, '-', 2)
        player_id = player_url[start+len('-'):]
        #for link in player_url:
        #start = time.time()
        df_receiving, df_defense, df_fumble, df_scoring, df_passing, df_rushing = PullPlayerStats_FootballDB(player_url, year)
        #end = time.time()
        #print(rf'{player} done. Took: {end - start} seconds')
        print('next')
        
    if not os.path.exists('FootballDB_database'):
        os.makedirs('FootballDB_database')
        
    #TODO: Create a way to update to DB after each loop
    #TODO: Missing BYE weeks on the player stats from FootballDB
        
    #TODO: Output to a new db
    #TODO: Loop through every player in the db and add their stats for every week
    # https://www.footballdb.com/teams/index.html
    
    print('done')