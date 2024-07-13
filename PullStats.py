from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from io import BytesIO




def Output(standings_df, week_list):
    user_df = pd.DataFrame()
    user_df['Team'] = standings_df.index.tolist()
    user_df = user_df.set_index('Team')
    user_df['Win Pct'] = standings_df['PCT'].tolist()
    user_df['Opp'] = week_list

    opp_pct = []
    for i in user_df['Opp']:
        if '@' in i:
            i = i[1:]
        opp_pct.append(standings_df.loc[i,'PCT'])
    user_df['Opp Pct'] = opp_pct

    user_df['Delta'] = user_df['Win Pct'].astype(float) - user_df['Opp Pct'].astype(float)

    print(user_df.sort_values(by='Delta', ascending=False))
    return user_df


def standings(lk_table):
    url = 'https://www.nfl.com/standings/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))



    #  Looking for the table with the classes 'wikitable' and 'sortable'
    table = soup.find('table', class_='d3-o-table')
    table_headers=[]
    conf_list = []
    exec = 0
    for x in soup.find_all('th'):
        if exec < 2:
            if 'AFC' in x.text.strip() or 'NFC' in x.text.strip():
                if exec < 1:
                    table_headers.append('Team')
                conf_list.append(x.text.strip())
                exec += 1
                continue
            table_headers.append(x.text.strip())
        if 'AFC' in x.text.strip() or 'NFC' in x.text.strip():
            conf_list.append(x.text.strip())

    df_conf_list = []

    for i in range(0,len(conf_list)):
        for j in range(0,4):
            df_conf_list.append(conf_list[i])

    final = []
    for table in soup.find_all('table'):
        for row in table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')
            row_list=[]
            if(columns != []):
                for i in range(0,len(columns)):
                    data = columns[i].text.strip()
                    if '\n' in columns[i].text.strip():
                        data = data[:data.find('\n')]
                    row_list.append(data)
            final.append(row_list)
    df1 = pd.DataFrame(final,columns = table_headers)
    df1['Conference']=df_conf_list
    df1['GP'] = df1['W'].astype(int) + df1['L'].astype(int) + df1['T'].astype(int)
    acronym_df1 = df1.replace(lk_table.keys(), lk_table.values())
    acronym_df1 = acronym_df1.sort_values(by='Team', ascending=True)
    acronym_df1 = acronym_df1.set_index('Team')

    return acronym_df1.sort_values(by='Team', ascending=True)


def DF_Creator(url, lk_table_mascot):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))



    #  Looking for the table with the classes 'wikitable' and 'sortable'
    table = soup.find('table', class_='d3-o-table')
    table_headers=[]
    for x in soup.find_all('th'):
        table_headers.append(x.text.strip())

    final = []
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        row_list=[]
        if(columns != []):
            for i in range(0,len(columns)):
                data = columns[i].text.strip()
                if '\n' in columns[i].text.strip():
                    data = data[:data.find('\n')]
                row_list.append(data)
        final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)

    acronym_df = df.replace(lk_table_mascot.keys(), lk_table_mascot.values())
    acronym_df = acronym_df.set_index('Team')
    return acronym_df.sort_values(by='Team', ascending=True)

def Player_DF_Creator(url, lk_table_mascot):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))



    #  Looking for the table with the classes 'wikitable' and 'sortable'
    table = soup.find('table', class_='TableBase-table')
    table_headers=[]
    for x in soup.find_all('th'):
        data = x.text.strip()
        if '\n' in data:
            data = data[:data.find('\n')]
        table_headers.append(data)
        

    final = []
    team_list=[]
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        row_list=[]
        if(columns != []):
            for i in range(0,len(columns)):
                data = columns[i].text.strip()
                if '\n' in data:
                    if i == 0:
                        start = find_nth(data, '\n', 7)
                        team = data[start+len('\n'):]
                        team_list.append(re.sub(r"^\s+", '', team))
                        start = find_nth(data, '\n', 4)
                    data = data[start+len('\n'):]
                    data = data[:data.find('\n')]
                if ' ' in data:
                    data = re.sub(r"^\s+", '', data)
                row_list.append(data)
        final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
    df['Team'] = team_list
    return df

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def Player_DF_Creator_NFL(url, lk_table_mascot):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))



    #  Looking for the table with the classes 'wikitable' and 'sortable'
    table = soup.find('table', class_='d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable')
    table_headers=[]
    for x in soup.find_all('th'):
        data = x.text.strip()
        if '\n' in data:
            data = data[:data.find('\n')]
        table_headers.append(data)
        

    final = []
    team_list=[]
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        row_list=[]
        if(columns != []):
            for i in range(0,len(columns)):
                data = columns[i].text.strip()
                if '\n' in data:
                    if i == 0:
                        start = find_nth(data, '\n', 7)
                        team = data[start+len('\n'):]
                        team_list.append(re.sub(r"^\s+", '', team))
                        start = find_nth(data, '\n', 4)
                    data = data[start+len('\n'):]
                    data = data[:data.find('\n')]
                if ' ' in data:
                    data = re.sub(r"^\s+", '', data)
                row_list.append(data)
        final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
    #df['Team'] = team_list
    return df





    

def NFL_stats(lk_table_mascot):    

    url = 'https://www.nfl.com/stats/player-stats/category/passing/2023/reg/all/passingyards/desc'
    qb_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/passing/2023/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAogoAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNekE1SWl3aU16SXdNRFF5TlRVdE5USTJOeTA1TnpNeExUZ3hZemd0TkRnMk56TmtZMlZqTldVeUlpd2lNakF5TXlKZGZRPT0='
    qb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/passing/2023/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAgPgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFORE1pTENJek1qQXdOR00wWmkwME16TTNMVFEwT0RJdE9UQTBZeTFoTkRkbU9HUm1NV1EwTVdJaUxDSXlNREl6SWwxOQ=='
    qb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    qb_df = pd.concat([qb_df1,qb_df2,qb_df3]).reset_index(drop=True)
    print('qb_df Complete')
    
    url = 'https://www.nfl.com/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc'
    rb_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/rushing/2023/REG/all/rushingyards/DESC?aftercursor=AAAAGQAAABlAiSgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STRNRFVpTENJek1qQXdOR0UwTVMwME16Y3pMVFEyTVRVdE5qQmpZUzA1T0RKa01EY3dORFk0TkRFaUxDSXlNREl6SWwxOQ=='
    rb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/rushing/2023/REG/all/rushingyards/DESC?aftercursor=AAAAMgAAADJAelAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNakVpTENJek1qQXdORFEwWmkwME1qTXdMVEl6TmpBdE9HVXhOQzFrWW1KbE1XUmxaR1V4TWpBaUxDSXlNREl6SWwxOQ=='
    rb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    rb_df = pd.concat([rb_df1,rb_df2,rb_df3]).reset_index(drop=True)
    print('rb_df Complete')
    
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc'
    rec_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAGQAAABhAU8AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNPU0lzSWpNeU1EQTBZelJtTFRRek5ESXRNRGt4TlMweFlXWTNMV1ZqTlRCbU5ETTNPRGczWXlJc0lqSXdNak1pWFgwPQ=='
    rec_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAMgAAADJAT4AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STJNeUlzSWpNeU1EQTFNRFE1TFRRek5UY3ROakUxTmkwMk5UTm1MV1V6WXpKaU5tUXhZamxpWXlJc0lqSXdNak1pWFgwPQ=='
    rec_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAASwAAAEhASgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFNaUlzSWpNeU1EQTFOelF4TFRSak5UQXRPVEEwTUMwMk4yUTJMVEEwTWpZNU1XWmlOVE0xWVNJc0lqSXdNak1pWFgwPQ=='
    rec_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAZAAAAGNARQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNaUlzSWpNeU1EQTBPRFE1TFRRM016Z3ROemM1TVMwNVpqZzVMV1ExTlRaak5HSTFPV0k1WVNJc0lqSXdNak1pWFgwPQ=='
    rec_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAfQAAAHlAQYAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpOU0lzSWpNeU1EQTFNelJrTFRVNU1qZ3RNekl6Tmkwell6VTVMVE0wTTJGaU56TTJZMk5oTXlJc0lqSXdNak1pWFgwPQ=='
    rec_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAlgAAAJVAPQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlPU0lzSWpNeU1EQTBPRFF4TFRVeU5Ea3RNekUyTXkxbU9HWTFMVGN6WXpVMVpqaGhOV013WkNJc0lqSXdNak1pWFgwPQ=='
    rec_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAArwAAAKpAOQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOU0lzSWpNeU1EQTFNRFF4TFRVeU5EZ3RNemMwTmkxaU5XWmlMV0ZsTnpNM1pHUmtNVEUwTWlJc0lqSXdNak1pWFgwPQ=='
    rec_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAyAAAAMFANQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNU0lzSWpNeU1EQTFOalF4TFRSak1UUXRNakV4TmkxbE5tUTVMVGcwWTJKbE1tSmtZV05tTlNJc0lqSXdNak1pWFgwPQ=='
    rec_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAA4QAAANtAMQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOeUlzSWpNeU1EQTBaRFUxTFRSbE16RXRNakUxTXkwNU0yRTJMVFpqT1dSaU9UTmtPVGt5WlNJc0lqSXdNak1pWFgwPQ=='
    rec_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAA-gAAAPlALAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOQ0lzSWpNeU1EQTBNalExTFRSak1qWXRPVGd5TUMxbFpXTXlMVGsyTVRjeU1tRmxNemMwTWlJc0lqSXdNak1pWFgwPQ=='
    rec_df11 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABEwAAARJAJgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNU0lzSWpNeU1EQTBNalExTFRRek1EUXROalUyTmkxaU5XWmhMVE0xWWpsaE9HVm1NVEJpTUNJc0lqSXdNak1pWFgwPQ=='
    rec_df12 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABLAAAASlAIgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVJaXdpTXpJd01EVXdOREV0TlRRek9DMDNNRGMxTFRSbE1qVXRZVEV3TnpKalpUSm1OV0ZqSWl3aU1qQXlNeUpkZlE9PQ=='
    rec_df13 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABRQAAATpAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNJaXdpTXpJd01EVTNORGt0TkdNeE9DMDFNekkxTFRNeE56a3RaR1ExTWpGaE1UaGpOekEySWl3aU1qQXlNeUpkZlE9PQ=='
    rec_df14 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABXgAAAVJAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EVXlORGt0TkRNd01TMHlOVEk1TFRreE9UWXRaamRoWmpGbVpXTXhNekZqSWl3aU1qQXlNeUpkZlE9PQ=='
    rec_df15 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABdwAAAWVAEAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBJaXdpTXpJd01EVTNORGt0TkdNMk9DMHlNall3TFRWbE4yWXRNbVZtTlRGbVpEWTRZbVk0SWl3aU1qQXlNeUpkZlE9PQ=='
    rec_df16 = Player_DF_Creator_NFL(url, lk_table_mascot)
    rec_df = pd.concat([rec_df1, rec_df2, rec_df3, rec_df4, rec_df5, rec_df6, rec_df7, rec_df8, rec_df9, rec_df10, rec_df11, rec_df12, rec_df13, rec_df14, rec_df15, rec_df16]).reset_index(drop=True)
    print('rec_df Complete')
    
    
    url = 'https://www.nfl.com/stats/player-stats/category/tackles/2023/reg/all/defensivecombinetackles/desc'
    tack_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/tackles/2023/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAGQAAABlAXoAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNakl1TUNJc0lqTXlNREEwTWpVNUxUUXhNalV0TVRNMk1TMW1OR0psTFdSaU1qazBZemhrT1dFd1ppSXNJakl3TWpNaVhYMD0='
    tack_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/tackles/2023/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAMgAAADJAWoAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNRFl1TUNJc0lqTXlNREEwTXpReExUVXpNekV0TmpFNE5TMHlZak0zTFRCa056RXlNR0pqT1RJeE1pSXNJakl3TWpNaVhYMD0='
    tack_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/tackles/2023/REG/all/defensivecombinetackles/DESC?aftercursor=AAAASwAAAEtAVwAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVNaTR3SWl3aU16SXdNRFV3TkRndE5Ea3lNUzAxTVRReUxUVmxaalV0TVRNellUTTJaR1JoTnpKbUlpd2lNakF5TXlKZGZRPT0='
    tack_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
    tack_df = pd.concat([tack_df1,tack_df2,tack_df3,tack_df4]).reset_index(drop=True)
    print('tack_df Complete')
    
    
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/reg/all/defensiveforcedfumble/desc'
    fum_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAGQAAAAtACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUmpORFV0TlRjME1TMDVOVGszTFRZMllXSXRZakU0WkRWbVlqWTFPV0UxSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAMgAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUTBOREV0TlRZME1pMDROVGt5TFRrNU16WXRNRGM0T1RabU5UVTVNV05qSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAASwAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EVXdOREV0TlRreE5pMDRPVGcyTFdRNVptSXRaRFZqWWpGa01UZGxZalF5SWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAlgAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTFORFF0TlRjMk9DMDROelkzTFdOaU1XVXROVEJrWWpKaFlXWmhaRFUySWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAArwAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTNOVEl0TkRVek9TMDNPVFE0TFRaak9EVXRaalJoWm1RMk1XWmhaR1EySWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
    fum_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
    fum_df = pd.concat([fum_df1,fum_df2,fum_df3,fum_df4,fum_df5,fum_df6,fum_df7,fum_df8,fum_df9,fum_df10]).reset_index(drop=True)
    print('fum_df Complete')
    
    
    url = 'https://www.nfl.com/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc'
    int_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/interceptions/2023/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAGQAAABlACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUXhORFF0TkRFMk55MDVOVFV3TFRGa05UUXRNekUwWXpJNE56TXlPVFE0SWl3aU1qQXlNeUpkZlE9PQ=='
    int_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/interceptions/2023/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAMgAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUXlOVEl0TkdZM015MDVNVFUzTFRSaE16Y3RZMkkxWlRobFlXUTJNR1F4SWl3aU1qQXlNeUpkZlE9PQ=='
    int_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/interceptions/2023/REG/all/defensiveinterceptions/DESC?aftercursor=AAAASwAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUmhOR1l0TkdVeE1DMHlNVFV4TFRGalpqa3ROalkyTlRFMU1Ua3hZV0UxSWl3aU1qQXlNeUpkZlE9PQ=='
    int_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
    int_df = pd.concat([int_df1,int_df2,int_df3,int_df4]).reset_index(drop=True)
    print('int_df Complete')

    url = 'https://www.nfl.com/stats/player-stats/category/field-goals/2023/reg/all/kickingfgmade/desc'
    fg_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/field-goals/2023/REG/all/kickingfgmade/DESC?aftercursor=AAAAGQAAABhAOAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOQ0lzSWpNeU1EQTBZVFJtTFRVek1qQXRPRFEyTkMwMFptUmhMVFF3TnpFM1pXUTVOMlJoWlNJc0lqSXdNak1pWFgwPQ=='
    fg_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/fumbles/2023/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAMgAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUTBOREV0TlRZME1pMDROVGt5TFRrNU16WXRNRGM0T1RabU5UVTVNV05qSWl3aU1qQXlNeUpkZlE9PQ=='
    fg_df = pd.concat([fg_df1,fg_df2]).reset_index(drop=True)
    print('fum_df Complete')
    
    url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/2023/reg/all/kickofftotal/desc'
    ko_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/2023/REG/all/kickofftotal/DESC?aftercursor=AAAAGQAAABdAUwAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNOaUlzSWpNeU1EQTFNelF4TFRSbE56a3ROakk1T1MwNE5USmxMV0l4TnpkbFpXVTVNamM0TUNJc0lqSXdNak1pWFgwPQ=='
    ko_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    ko_df = pd.concat([ko_df1,ko_df2]).reset_index(drop=True)
    print('ko_df Complete')

    url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2023/reg/all/kickreturnsaverageyards/desc'
    kor_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2023/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAGQAAABlAOQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOUzR3SWl3aU16SXdNRFE1TlRNdE5ERTFOaTB5TnpJeUxXSm1Nall0TmpJeE9ERXpOVEZoTWpJMElpd2lNakF5TXlKZGZRPT0='
    kor_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2023/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJANVR64UeuFDFleUp6WldGeVkyaEJablJsY2lJNld5SXlNUzR6TXlJc0lqTXlNREEwTWpSbUxUVTNNRFl0T0RZMk9DMWlORE01TFdFNU9UTmhZekJsT1dRMVpDSXNJakl3TWpNaVhYMD0='
    kor_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2023/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAASwAAAEtAMQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOeTR3SWl3aU16SXdNRFF4TkdNdE5HTXhNQzA0T1RreExUSTVOVFV0WWpWaU5qSTRPR001WVdabElpd2lNakF5TXlKZGZRPT0='
    kor_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/2023/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAZAAAAGJAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNMakFpTENJek1qQXdOV0UwTVMwME16RXpMVE14T0RBdFltRXdNUzFoWlRneE1ETXpNVFJtWVRJaUxDSXlNREl6SWwxOQ=='
    kor_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
    kor_df = pd.concat([kor_df1,kor_df2,kor_df3,kor_df4,kor_df5]).reset_index(drop=True)
    print('kor_df Complete')
    
    url = 'https://www.nfl.com/stats/player-stats/category/punts/2023/reg/all/puntingaverageyards/desc'
    punt_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://nfl.com/stats/player-stats/category/punts/2023/REG/all/puntingaverageyards/DESC?aftercursor=AAAAGQAAABlARxrhR64UezFleUp6WldGeVkyaEJablJsY2lJNld5STBOaTR5TVNJc0lqTXlNREExTnpRNExUUTFOelV0TlRNMk5TMWxPVFF4TFRWaFpqUTJZMlV4WmpKa01TSXNJakl3TWpNaVhYMD0='
    punt_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    punt_df = pd.concat([punt_df1,punt_df2]).reset_index(drop=True)
    print('punt_df Complete')

    url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/2023/reg/all/puntreturnsaverageyards/desc'
    puntr_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/2023/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAGQAAABlAI4AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVMamMxSWl3aU16SXdNRFEwTkRFdE5USXlOaTB4TXpRMkxUaG1ORFV0T0dRd1lXSTNOakU0WVRrNUlpd2lNakF5TXlKZGZRPT0='
    puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/2023/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJAHZmZmZmZmjFleUp6WldGeVkyaEJablJsY2lJNld5STNMalFpTENJek1qQXdOVE0wT0MwME1URXdMVGMwTWpjdFpqTTBZUzFpWWpCaFlURmtPR1UxTlRZaUxDSXlNREl6SWwxOQ=='
    puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
    puntr_df = pd.concat([puntr_df1,puntr_df2]).reset_index(drop=True)
    print('puntr_df Complete')





    print('Complete')

    return qb_df, rb_df, rec_df, int_df, fg_df, ko_df, kor_df, punt_df, puntr_df, fum_df

def NFL_stats_off(lk_table_mascot):
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/2023/reg/all'
    passing_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/rushing/2023/reg/all'
    rushing_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/receiving/2023/reg/all'
    receiving_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/scoring/2023/reg/all'
    scoring_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/downs/2023/reg/all'
    downs_off_df = DF_Creator(url, lk_table_mascot)
    print('teams offense complete')
    return passing_off_df, rushing_off_df, receiving_off_df, scoring_off_df, downs_off_df

def NFL_stats_def(lk_table_mascot):
    url = 'https://www.nfl.com/stats/team-stats/defense/passing/2023/reg/all'
    passing_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/rushing/2023/reg/all'
    rushing_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/receiving/2023/reg/all'
    receiving_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/scoring/2023/reg/all'
    scoring_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/tackles/2023/reg/all'
    tackles_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/downs/2023/reg/all'
    downs_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/fumbles/2023/reg/all'
    fumbles_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/interceptions/2023/reg/all'
    interception_def_df = DF_Creator(url, lk_table_mascot)
    print('teams defense complete')
    return passing_def_df, rushing_def_df, receiving_def_df, scoring_def_df, tackles_def_df, downs_def_df, fumbles_def_df, interception_def_df

def NFL_stats_st(lk_table_mascot):
    url = 'https://www.nfl.com/stats/team-stats/special-teams/field-goals/2023/reg/all'
    special_fg_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/scoring/2023/reg/all'
    special_scoring_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/kickoffs/2023/reg/all'
    special_kickoff_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/kickoff-returns/2023/reg/all'
    special_kickoff_return_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/punts/2023/reg/all'
    special_punting_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/punt-returns/2023/reg/all'
    special_punting_returns_df = DF_Creator(url, lk_table_mascot)
    print('teams special teams complete')
    return special_fg_df, special_scoring_df, special_kickoff_df, special_kickoff_return_df, special_punting_df, special_punting_returns_df

def CBS_Stats(lk_table_mascot):
    ##########################################
    #CBS STARTS HERE
    ##########################################

    url = 'https://www.cbssports.com/nfl/stats/player/rushing/nfl/regular/qualifiers/?page=1'
    rush_df1 = Player_DF_Creator(url, lk_table_mascot)
    url = 'https://www.cbssports.com/nfl/stats/player/rushing/nfl/regular/qualifiers/?page=2'
    rush_df2 = Player_DF_Creator(url, lk_table_mascot)
    rush_df = pd.concat([rush_df1,rush_df2]).reset_index(drop=True)
    rush_yd_per_gp_df = rush_df.sort_values(by='YDS/G', ascending=False).reset_index(drop=True)
    print(rush_yd_per_gp_df)

    url = 'https://cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/?page=1'
    pass_df1 = Player_DF_Creator(url, lk_table_mascot)
    url = 'https://cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/?page=2'
    pass_df2 = Player_DF_Creator(url, lk_table_mascot)
    pass_df = pd.concat([pass_df1,pass_df2]).reset_index(drop=True)

    url = 'https://www.cbssports.com/nfl/stats/player/receiving/nfl/regular/qualifiers/?page=1'
    rec_df1 = Player_DF_Creator(url, lk_table_mascot)
    url = 'https://www.cbssports.com/nfl/stats/player/receiving/nfl/regular/qualifiers/?page=2'
    rec_df2 = Player_DF_Creator(url, lk_table_mascot)
    rec_df_cbs = pd.concat([rec_df1,rec_df2]).reset_index(drop=True)
    rec_df_cbs['REC/GP'] = rec_df_cbs['REC'].astype(int) / rec_df_cbs['GP'].astype(int)
    rec_rec_per_gp_df = rec_df_cbs.sort_values(by='REC/GP', ascending=False).reset_index(drop=True)



    url = 'https://www.cbssports.com/nfl/stats/player/kicking/nfl/regular/qualifiers/'
    kick_df1= Player_DF_Creator(url, lk_table_mascot).reset_index(drop=True)

    url = 'https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/?page=1'
    score_df1 = Player_DF_Creator(url, lk_table_mascot)
    url = 'https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/?page=2'
    score_df2 = Player_DF_Creator(url, lk_table_mascot)
    url = 'https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/?page=3'
    score_df3 = Player_DF_Creator(url, lk_table_mascot)
    score_df = pd.concat([score_df1,score_df2, score_df3]).reset_index(drop=True)

    # url = 'https://www.cbssports.com/nfl/stats/player/defense/nfl/regular/qualifiers/?page=1'
    # def_df1 = Player_DF_Creator(url, lk_table_mascot)
    # url = 'https://www.cbssports.com/nfl/stats/player/defense/nfl/regular/qualifiers/?page=2'
    # def_df2 = Player_DF_Creator(url, lk_table_mascot)
    # url = 'https://www.cbssports.com/nfl/stats/player/defense/nfl/regular/qualifiers/?page=3'
    # def_df3 = Player_DF_Creator(url, lk_table_mascot)
    # def_df = pd.concat([def_df1,def_df2, def_df3])

    url = 'https://www.nfl.com/stats/team-stats/defense/passing/2023/reg/all'
    passing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/rushing/2023/reg/all'
    rushing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/2023/reg/all'
    passing_of = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/rushing/2023/reg/all'
    rushing_of = DF_Creator(url, lk_table_mascot)
    print('Complete')

    return rush_df, rush_yd_per_gp_df, pass_df, rec_df_cbs, rec_rec_per_gp_df, kick_df1, score_df, passing_df, rushing_df, passing_of, rushing_of



if __name__ == '__main__':
    
    import PullRosters
    import utils
    
    week_list, lk_table_mascot, lk_table, NFL_URLs = utils.init()
    standings_df = standings(lk_table)
    
    (qb_df, rb_df, rec_df) = NFL_stats(lk_table_mascot)
    (rush_df, rush_yd_per_gp_df, pass_df, rec_df_cbs, rec_rec_per_gp_df, kick_df1, score_df, passing_df, rushing_df, passing_of, rushing_of) = CBS_Stats(lk_table_mascot)
    
    output = Output(standings_df, week_list)