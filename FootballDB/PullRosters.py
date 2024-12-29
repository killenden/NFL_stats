from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os




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
        headers_list.append(header.text)
        
    df_final = pd.DataFrame(columns=headers_list)
        
    player_dict = {}
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
                    player_dict[data.contents[0].contents[0].contents[0].text] = data.contents[0].contents[0].contents[0].attrs['href']
            except:
                data_list.append(data.text)
                continue
                    
        
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
        
    #TODO: Output to a new db
    #TODO: Loop through every player in the db and add their stats for every week
    # https://www.footballdb.com/teams/index.html
    
    print('done')