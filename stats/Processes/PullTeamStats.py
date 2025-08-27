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
                    data_list.append(data.text[:end].replace("\u00A0", " "))
                    player_dict[data.contents[0].contents[0].contents[0].text] = data.contents[0].contents[0].contents[0].attrs['href'].replace("\u00A0", " ")
            except:
                if len(data_list) == position_index:
                    if data.text in ['QB', 'RB', 'WR', 'TE']: # Add more positions as needed
                        data_list.append(data.text.replace("\u00A0", " "))
                    else:
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

def FindHeaders(stats):
    headers_list = []
    colspan_list = []
    #headers_list.append('Type')
    if len(stats.contents) > 0:
        for table in stats.contents:
            try:
                if 'thead' == table.name:
                    try:
                        for headers in table.contents:
                            try:
                                if headers.attrs['class'] == ['header', 'center']:
                                    for header in headers.contents:
                                        if header.text == '\n':
                                            continue
                                        if FindColSpan(header) > 0:
                                            for i in range(0,FindColSpan(header)):
                                                colspan_list.append(header.text.replace("\u00A0", " "))
                                        else:
                                            colspan_list.append('')
                                if headers.attrs['class'] == ['header', 'right']:
                                    i = 0
                                    for header in headers.contents:
                                        if not '\n' == header.text:
                                            try:
                                                if colspan_list[i] != '':
                                                    #headers_list.append(f'{colspan_list[i]} {header.text.replace("\u00A0", " ")}')
                                                    headers_list.append(f'{colspan_list[i]} {header.text.replace("u00A0", " ")}')
                                                else:
                                                    headers_list.append(header.text.replace("\u00A0", " "))
                                                i += 1
                                            except:
                                                headers_list.append(header.text.replace("\u00A0", " "))
                                    return headers_list
                            except:
                                continue
                    except:
                        continue
            except:
                continue
    else:
        return headers_list

def FindHeaders1(player_stats):
    headers_list = []
    headers_list.append('Type')
    if len(player_stats.contents) > 0:
        for table in player_stats.contents:
            try:
                for player_info in table.contents:
                    try:
                        if 'thead' == player_info.name:
                            for headers in player_info.contents:
                                try:
                                    if headers.attrs['class'] == ['header', 'right']:
                                        for header in headers.contents:
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

def FindTeamStats(stats, headers_list):
    
    player_statistics_dict = {}
    #headers_list.append('Type')
    if len(stats.contents) > 0:
        for table in stats.contents:
            try:
                if 'tbody' == table.name:
                    try:
                        for data in table.contents:
                            statistics = []
                            try:
                                if not '\n' == data.text:
                                    for header in data.contents:
                                        if not '\n' == header.text:
                                            if len(header.contents) != 0:
                                                statistics.append(header.contents[0].text.replace("\u00A0", " "))
                                            else:
                                                statistics.append(header.text.replace("\u00A0", " "))
                                    try:
                                        
                                        df_final = pd.concat([pd.DataFrame([statistics], columns=headers_list), df_final], ignore_index=True).reset_index(drop=True)
                                    except:
                                        df_final = pd.DataFrame([statistics], columns=headers_list)
                            except:
                                continue
                        return df_final
                    except:
                        continue
            except:
                continue
    else:
        return None

def FindPlayersStats1(player_stats):
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


def PullTeamStats_FootballDB(year):
    start = time.time()
    category_dict = {'Overall': 'T',
                    'Passing': 'P',
                    'Rushing': 'R',
                    'Kickoff Returns': 'KR',
                    'Punt Returns': 'PR',
                    'Punting': 'U',
                    'Scoring': 'S',
                    'Downs': 'W'}
        
    group_dict = {'Offense': 'O',
                'Defense': 'D'}
    
    #used for webscraping
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    for group, group_code in group_dict.items():
        for category, category_code in category_dict.items():
            r = requests.get(rf'https://www.footballdb.com/stats/teamstat.html?lg=NFL&yr={year}&type=reg&cat={category_code}&group={group_code}&conf=', headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            footballdb_dict = {}
            roster_links = []
    
            df_final = None
            for team_stats in soup.find_all('table'):
                headers_list = FindHeaders(team_stats)
                #print('Headers found')
                df_final = FindTeamStats(team_stats, headers_list)
                df_final.set_index('Team', inplace=True)
                break
            
            
            if rf'{group} {category}' == 'Offense Overall':
                df_offense_overall = df_final
            elif rf'{group} {category}' == 'Offense Passing':
                df_offense_passing = df_final
            elif rf'{group} {category}' == 'Offense Rushing':
                df_offense_rushing = df_final
            elif rf'{group} {category}' == 'Offense Kickoff Returns':
                df_offense_kickoff_returns = df_final
            elif rf'{group} {category}' == 'Offense Punt Returns':
                df_offense_punt_returns = df_final
            elif rf'{group} {category}' == 'Offense Punting':
                df_offense_punting = df_final
            elif rf'{group} {category}' == 'Offense Scoring':
                df_offense_scoring = df_final
            elif rf'{group} {category}' == 'Offense Downs':
                df_offense_downs = df_final
            elif rf'{group} {category}' == 'Defense Overall':
                df_defense_overall = df_final
            elif rf'{group} {category}' == 'Defense Passing':
                df_defense_passing = df_final
            elif rf'{group} {category}' == 'Defense Rushing':
                df_defense_rushing = df_final
            elif rf'{group} {category}' == 'Defense Kickoff Returns':
                df_defense_kickoff_returns = df_final
            elif rf'{group} {category}' == 'Defense Punt Returns':
                df_defense_punt_returns = df_final
            elif rf'{group} {category}' == 'Defense Punting':
                df_defense_punting = df_final
            elif rf'{group} {category}' == 'Defense Scoring':
                df_defense_scoring = df_final
            elif rf'{group} {category}' == 'Defense Downs':
                df_defense_downs = df_final
    end = time.time()
    print(rf'done. Took: {end - start} seconds')
    return (df_offense_overall, df_offense_passing, df_offense_rushing, df_offense_kickoff_returns, 
        df_offense_punt_returns, df_offense_punting, df_offense_scoring, df_offense_downs,
        df_defense_overall, df_defense_passing, df_defense_rushing, df_defense_kickoff_returns, 
        df_defense_punt_returns, df_defense_punting, df_defense_scoring, df_defense_downs)


if __name__ == '__main__':
    
    PullTeamStats_FootballDB('2024')
    
    print('done')