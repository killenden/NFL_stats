from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import time



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
                    player_dict[data.contents[0].contents[0].contents[0].text] = data.contents[0].contents[0].contents[0].attrs['href']
            except:
                if len(data_list) == position_index:
                    if data.text in ['QB', 'RB', 'WR', 'TE']: # Add more positions as needed
                        data_list.append(data.text)
                    else:
                        data_list = []
                        break
                else:
                    data_list.append(data.text)
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

def FindHeaders(player_stats):
    headers_list = []
    colspan_list = []
    headers_list.append('Type')
    if len(player_stats.contents) > 0:
        for table in player_stats.contents:
            try:
                for player_info in table.contents:
                    try:
                        if 'thead' == player_info.name:
                            for headers in player_info.contents:
                                try:
                                    if headers.attrs['class'] == ['header', 'center']:
                                        for header in headers.contents:
                                            if header.text == '\n':
                                                continue
                                            if FindColSpan(header) > 0:
                                                for i in range(0,FindColSpan(header)):
                                                    colspan_list.append(header.text)
                                            else:
                                                colspan_list.append('')
                                    if headers.attrs['class'] == ['header', 'right']:
                                        i = 0
                                        for header in headers.contents:
                                            if not '\n' == header.text:
                                                try:
                                                    if colspan_list[i] != '':
                                                        headers_list.append(f'{colspan_list[i]} {header.text}')
                                                    else:
                                                        headers_list.append(header.text)
                                                    i += 1
                                                except:
                                                    headers_list.append(header.text)
                                        return headers_list
                                except:
                                    continue
                    except:
                        continue
            except:
                continue
    else:
        return headers_list

def FindColSpan(stat):
    try:
        return int(stat.attrs['colspan'])
    except:
        return 0
    
def CreateStatsList(stats, player_statistics):
    for stat in stats.contents:
        if FindColSpan(stat) > 0:
            for i in range(0,FindColSpan(stat)):
                player_statistics.append(stat.text)
        else:
            player_statistics.append(stat.text)
    return player_statistics

def FindPlayersStats(player_stats):
    player_statistics = []
    player_statistics_dict = {}
    i = 1
    reset_week_count = False
    if len(player_stats.contents) > 0:
        for table in player_stats.contents:
            try:
                for player_info in table.contents:
                    try:
                        if 'tbody' == player_info.name:
                            for stats in player_info.contents:
                                try:
                                    player_statistics = []
                                    if stats.attrs['class'][1] == 'preseason':
                                        player_statistics.append('Preseason')
                                        player_statistics_dict[rf'Preseason Week {i}'] = CreateStatsList(stats, player_statistics)
                                        i += 1
                                        reset_week_count = True
                                    else:
                                        if i > 1 and reset_week_count == True:
                                            i = 1
                                            reset_week_count = False
                                        player_statistics.append('Regular')
                                        player_statistics_dict[rf'Regular Week {i}'] = CreateStatsList(stats, player_statistics)
                                    try:
                                        if player_statistics_dict[rf'Regular Week {i}'][1] == 'TOTALS':
                                            del player_statistics_dict[rf'Regular Week {i}']
                                            return player_statistics_dict
                                    except:
                                        continue
                                    i += 1
                                except:
                                    continue
                    except:
                        continue
            except:
                continue
    else:
        return player_statistics_dict


def PullPlayerStats_FootballDB(player, player_url, year):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    
    r = requests.get(rf'https://www.footballdb.com{player_url}/gamelogs/{year}', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    footballdb_dict = {}
    roster_links = []
    
    game_logs = [rf'{year} Receiving Game Logs', rf'{year} Fumble Game Logs', rf'{year} Passing Game Logs', rf'{year} Rushing Game Logs']
    #game_logs = [rf'{year} Receiving Game Logs', rf'{year} Defense Game Logs', rf'{year} Fumble Game Logs', rf'{year} Scoring Game Logs', rf'{year} Passing Game Logs', rf'{year} Rushing Game Logs']
    
    
    for game_log in game_logs:
        df_final = None
        for player_stats in soup.find_all('div', {'data-title': game_log}):
            headers_list = FindHeaders(player_stats)
            #print('Headers found')
            start = find_nth(player_url, '-', 2)
            player_id = player_url[start+len('-'):]
            player_stats_list = FindPlayersStats(player_stats)
            #print('Player Stats found')
            if player_stats_list == None:
                return None, None, None, None
            else:
                df_final = pd.DataFrame(player_stats_list).T
                df_final.columns=headers_list
            break
        
        if 'Receiving' in game_log:
            df_receiving = df_final
        elif 'Defense' in game_log:
            df_defense = df_final
        elif 'Fumble' in game_log:
            df_fumble = df_final
        elif 'Scoring' in game_log:
            df_scoring = df_final
        elif 'Passing' in game_log:
            df_passing = df_final
        elif 'Rushing' in game_log:
            df_rushing = df_final
    return df_receiving, df_fumble, df_passing, df_rushing
    #return df_receiving, df_defense, df_fumble, df_scoring, df_passing, df_rushing

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
        
    #TODO: Create a way to update to DB after each loop
    #TODO: Missing BYE weeks on the player stats from FootballDB
        
    #TODO: Output to a new db
    #TODO: Loop through every player in the db and add their stats for every week
    # https://www.footballdb.com/teams/index.html
    
    print('done')