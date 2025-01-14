from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
from PullPlayerStats import *
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database import *




def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def find_nth_capital(input_string, n):
    count = 0
    
    for idx, char in enumerate(input_string):
        if char.isupper():
            count += 1
            if count == n:
                return idx
    
    return -1  # Return -1 if nth capital letter is not found

def PullTeam_FootballDB(url, team):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))
    
    #  Looking for the table with the classes 'wikitable' and 'sortable'
    
    headers_list = []
    headers_list.append('Team')
    #table = soup.find('table', class_='d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-table--sortable')
    for header in soup.find_all(class_ = 'thead')[0].contents:
        headers_list.append(header.text.replace("\u00A0", " "))
        
    df_final = pd.DataFrame(columns=headers_list)
        
    player_dict = {}
    position_index = headers_list.index('Pos')
    for row in soup.find_all(class_ = 'tr'):
        data_list = []
        data_list.append(team)
        for data in row.contents:
            # if '\n' in data.text:
            #     end = find_nth(data.text, '\n', 0)
            #     data_list.append(data.text[:end])
            # else:
            #     data_list.append(data.text)
            try:
                if data.contents[0].attrs['class'][0] == 'rostplayer':
                    end = find_nth(data.text, '\n', 0)
                    data_list.append(data.text[:end])
                    name = data.contents[0].contents[0].contents[0].text.replace("\u00A0", " ")
                    player_dict[name] = data.contents[0].contents[0].contents[0].attrs['href'].replace("\u00A0", " ")
                    
            except:
                if len(data_list) == position_index:
                    if data.text in ['QB', 'RB', 'WR', 'TE']: # Add more positions as needed
                        data_list.append(data.text.replace("\u00A0", " "))
                    else:
                        del player_dict[name]
                        data_list = []
                        break
                else:
                    data_list.append(data.text.replace("\u00A0", " "))
                continue
        if len(data_list) > 1:
            df_final = pd.concat([pd.DataFrame([data_list], columns=headers_list), df_final], ignore_index=True).reset_index(drop=True)
    # for i in range(1,len(soup.find_all('h4'))):
        
    #     if i != 1:
    #         table = SwitchTables(table)
        
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    
    # for table in soup.find_all('table'):
    #     table = soup.find('table', class_='TableBase-table')
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    return df_final, player_dict

def ScrapingFootballDB(soup):
    footballdb_dict = {}
    roster_links = []
    for team in soup.find_all(class_ = 'teams-item teams-league-NFL'):
        for team_info in team.contents:
            try:
                if 'teams-infobox' in team_info.attrs['class'][0]:
                    for info in team_info.contents:
                        try:
                            if 'teams-teamname' in info.attrs['class'][0]:
                                team_name = info.contents[0].text.replace("\u00A0", " ")
                            if 'teams-teamlinks' in info.attrs['class'][0]:
                                for link in info.contents:
                                    try:
                                        if 'roster' in link.attrs['title'].lower():
                                            footballdb_dict[team_name] = link.attrs['href'].replace("\u00A0", " ")
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
        
    return df_final, player_dict_final

if __name__ == '__main__':
    
    #used for webscraping
    
    
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
        
    #TODO: Create a way to update to DB after each loop
    #TODO: Missing BYE weeks on the player stats from FootballDB
        
    #TODO: Output to a new db
    #TODO: Loop through every player in the db and add their stats for every week
    # https://www.footballdb.com/teams/index.html
    
    print('done')