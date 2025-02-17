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

def find_next_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    next_page_link = soup.find('a', class_='nfl-o-table-pagination__next')
    
    return next_page_link.attrs['href']


def loop_urls(lk_table_mascot,url,max_pages=20):
    df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
    first_loop = True
    for i in range(0,max_pages):
        try:
            url_next = find_next_url(url)
            url = 'https://www.nfl.com'+url_next
            df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
            if first_loop:
                df = pd.concat([df1,df2]).reset_index(drop=True)
            else:
                df = pd.concat([df,df2]).reset_index(drop=True)
            first_loop = False
        except:
            break
    return df

def NFL_stats(lk_table_mascot, year):    
    year = str(year)
    if year != '2024':
        url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/reg/all/passingyards/desc'
        qb_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url_next = find_next_url(url)
        url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAogoAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNekE1SWl3aU16SXdNRFF5TlRVdE5USTJOeTA1TnpNeExUZ3hZemd0TkRnMk56TmtZMlZqTldVeUlpd2lNakF5TXlKZGZRPT0='
        qb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAgPgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFORE1pTENJek1qQXdOR00wWmkwME16TTNMVFEwT0RJdE9UQTBZeTFoTkRkbU9HUm1NV1EwTVdJaUxDSXlNREl6SWwxOQ=='
        qb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        qb_df = pd.concat([qb_df1,qb_df2,qb_df3]).reset_index(drop=True)
        print('qb_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/reg/all/rushingyards/desc'
        rb_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAGQAAABlAiSgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STRNRFVpTENJek1qQXdOR0UwTVMwME16Y3pMVFEyTVRVdE5qQmpZUzA1T0RKa01EY3dORFk0TkRFaUxDSXlNREl6SWwxOQ=='
        rb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAMgAAADJAelAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNakVpTENJek1qQXdORFEwWmkwME1qTXdMVEl6TmpBdE9HVXhOQzFrWW1KbE1XUmxaR1V4TWpBaUxDSXlNREl6SWwxOQ=='
        rb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAASwAAAEtAboAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlORFFpTENJek1qQXdOR1ExTlMwMU1qWTNMVEEwTVRNdE9HUXpOaTFoTldNelptUTNPREZoWVRBaUxDSXlNREl6SWwxOQ=='
        rb_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAZAAAAGRAY4AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOVFlpTENJek1qQXdOR1EwT1MwMFl6TTJMVGt3T0RVdE4ySTBNQzAyTnpKaU5EY3pNMk5pWXpZaUxDSXlNREl6SWwxOQ=='
        rb_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAfQAAAH1AV8AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVOU0lzSWpNeU1EQTBZVFJtTFRSbE56WXROREF4T0MwelpXVmpMV0UxWVRRNU1UWTBPVE00TWlJc0lqSXdNak1pWFgwPQ=='
        rb_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAlgAAAJZATgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STJNQ0lzSWpNeU1EQTBaRFF6TFRSaU5qVXROamMyTkMxbE5qZzFMVFppTURkbU5HUmlZV015T0NJc0lqSXdNak1pWFgwPQ=='
        rb_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAArwAAAKxARAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNQ0lzSWpNeU1EQTFOalF4TFRVMU5ESXRORGszT1MwME1UVmtMVGswTURObFlUYzVNMlk1WWlJc0lqSXdNak1pWFgwPQ=='
        rb_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAyAAAAMdAOQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOU0lzSWpNeU1EQTBaRFUxTFRSak5EZ3ROall4TWkxaU1ETmlMVFV3WmpobVl6WmhZbVV5TkNJc0lqSXdNak1pWFgwPQ=='
        rb_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAA4QAAAN5AMgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhPQ0lzSWpNeU1EQTFNRFE1TFRRek5UY3ROakUxTmkwMk5UTm1MV1V6WXpKaU5tUXhZamxpWXlJc0lqSXdNak1pWFgwPQ=='
        rb_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAA-gAAAPlAJAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNQ0lzSWpNeU1EQTBOalUxTFRSbE5qSXRNamt6TmkxallqZG1MVGc1TXpobU56Y3dOV1U0WVNJc0lqSXdNak1pWFgwPQ=='
        rb_df11 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAABEwAAARNAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EUXlOR1l0TlRrMk9TMDJOVGd3TFRNd1lXSXRNRGN6WWpjd1pHSmtORGhpSWl3aU1qQXlNeUpkZlE9PQ=='
        rb_df12 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAABLAAAASRAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EVTBOVFV0TlRJek1DMDBOamsxTFRVMllUZ3RZemRqTmprME1XVXdPV1k1SWl3aU1qQXlNeUpkZlE9PQ=='
        rb_df13 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAABRQAAATQAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EVmhORFV0TkdVM015MDRNREEwTFRnM09HRXRZVEUwTnpJNE9EQmlZVFpsSWl3aU1qQXlNeUpkZlE9PQ=='
        rb_df14 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAABWgAAAVrAKAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXRNVElpTENJek1qQXdOR0UwTlMwME5qSTJMVGt5T0RjdFl6UTFOQzAwTnpsaU9UUXlZMkprTWpZaUxDSXlNREl6SWwxOQ=='
        rb_df15 = Player_DF_Creator_NFL(url, lk_table_mascot)
        rb_df = pd.concat([rb_df1, rb_df2, rb_df3, rb_df4, rb_df5, rb_df6, rb_df7, rb_df8, rb_df9, rb_df10, rb_df11, rb_df12, rb_df13, rb_df14, rb_df15]).reset_index(drop=True)
        print('rb_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/reg/all/receivingreceptions/desc'
        rec_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAASwAAAElAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EUTFOVFl0TkRFMU15MDBNekE1TFdJeVpXUXRObUk0TWpNelpqWm1aV0UxSWl3aU1qQXlOQ0pkZlE9PQ=='
        rec_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAMgAAADJAT4AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STJNeUlzSWpNeU1EQTFNRFE1TFRRek5UY3ROakUxTmkwMk5UTm1MV1V6WXpKaU5tUXhZamxpWXlJc0lqSXdNak1pWFgwPQ=='
        rec_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAASwAAAEhASgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFNaUlzSWpNeU1EQTFOelF4TFRSak5UQXRPVEEwTUMwMk4yUTJMVEEwTWpZNU1XWmlOVE0xWVNJc0lqSXdNak1pWFgwPQ=='
        rec_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAZAAAAGNARQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNaUlzSWpNeU1EQTBPRFE1TFRRM016Z3ROemM1TVMwNVpqZzVMV1ExTlRaak5HSTFPV0k1WVNJc0lqSXdNak1pWFgwPQ=='
        rec_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAfQAAAHlAQYAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpOU0lzSWpNeU1EQTFNelJrTFRVNU1qZ3RNekl6Tmkwell6VTVMVE0wTTJGaU56TTJZMk5oTXlJc0lqSXdNak1pWFgwPQ=='
        rec_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAlgAAAJVAPQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlPU0lzSWpNeU1EQTBPRFF4TFRVeU5Ea3RNekUyTXkxbU9HWTFMVGN6WXpVMVpqaGhOV013WkNJc0lqSXdNak1pWFgwPQ=='
        rec_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAArwAAAKpAOQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOU0lzSWpNeU1EQTFNRFF4TFRVeU5EZ3RNemMwTmkxaU5XWmlMV0ZsTnpNM1pHUmtNVEUwTWlJc0lqSXdNak1pWFgwPQ=='
        rec_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAyAAAAMFANQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNU0lzSWpNeU1EQTFOalF4TFRSak1UUXRNakV4TmkxbE5tUTVMVGcwWTJKbE1tSmtZV05tTlNJc0lqSXdNak1pWFgwPQ=='
        rec_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAA4QAAANtAMQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOeUlzSWpNeU1EQTBaRFUxTFRSbE16RXRNakUxTXkwNU0yRTJMVFpqT1dSaU9UTmtPVGt5WlNJc0lqSXdNak1pWFgwPQ=='
        rec_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAA-gAAAPlALAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOQ0lzSWpNeU1EQTBNalExTFRSak1qWXRPVGd5TUMxbFpXTXlMVGsyTVRjeU1tRmxNemMwTWlJc0lqSXdNak1pWFgwPQ=='
        rec_df11 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAABEwAAARJAJgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNU0lzSWpNeU1EQTBNalExTFRRek1EUXROalUyTmkxaU5XWmhMVE0xWWpsaE9HVm1NVEJpTUNJc0lqSXdNak1pWFgwPQ=='
        rec_df12 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAABLAAAASlAIgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVJaXdpTXpJd01EVXdOREV0TlRRek9DMDNNRGMxTFRSbE1qVXRZVEV3TnpKalpUSm1OV0ZqSWl3aU1qQXlNeUpkZlE9PQ=='
        rec_df13 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAABRQAAATpAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNJaXdpTXpJd01EVTNORGt0TkdNeE9DMDFNekkxTFRNeE56a3RaR1ExTWpGaE1UaGpOekEySWl3aU1qQXlNeUpkZlE9PQ=='
        rec_df14 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAABXgAAAVJAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EVXlORGt0TkRNd01TMHlOVEk1TFRreE9UWXRaamRoWmpGbVpXTXhNekZqSWl3aU1qQXlNeUpkZlE9PQ=='
        rec_df15 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAABdwAAAWVAEAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBJaXdpTXpJd01EVTNORGt0TkdNMk9DMHlNall3TFRWbE4yWXRNbVZtTlRGbVpEWTRZbVk0SWl3aU1qQXlNeUpkZlE9PQ=='
        rec_df16 = Player_DF_Creator_NFL(url, lk_table_mascot)
        rec_df = pd.concat([rec_df1, rec_df2, rec_df3, rec_df4, rec_df5, rec_df6, rec_df7, rec_df8, rec_df9, rec_df10, rec_df11, rec_df12, rec_df13, rec_df14, rec_df15, rec_df16]).reset_index(drop=True)
        print('rec_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/reg/all/defensivecombinetackles/desc'
        tack_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAGQAAABlAXoAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNakl1TUNJc0lqTXlNREEwTWpVNUxUUXhNalV0TVRNMk1TMW1OR0psTFdSaU1qazBZemhrT1dFd1ppSXNJakl3TWpNaVhYMD0='
        tack_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAMgAAADJAWoAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNRFl1TUNJc0lqTXlNREEwTXpReExUVXpNekV0TmpFNE5TMHlZak0zTFRCa056RXlNR0pqT1RJeE1pSXNJakl3TWpNaVhYMD0='
        tack_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAASwAAAEtAVwAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVNaTR3SWl3aU16SXdNRFV3TkRndE5Ea3lNUzAxTVRReUxUVmxaalV0TVRNellUTTJaR1JoTnpKbUlpd2lNakF5TXlKZGZRPT0='
        tack_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        tack_df = pd.concat([tack_df1,tack_df2,tack_df3,tack_df4]).reset_index(drop=True)
        print('tack_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/reg/all/defensiveforcedfumble/desc'
        fum_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAGQAAAAtACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUmpORFV0TlRjME1TMDVOVGszTFRZMllXSXRZakU0WkRWbVlqWTFPV0UxSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAMgAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUTBOREV0TlRZME1pMDROVGt5TFRrNU16WXRNRGM0T1RabU5UVTVNV05qSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAASwAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EVXdOREV0TlRreE5pMDRPVGcyTFdRNVptSXRaRFZqWWpGa01UZGxZalF5SWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAlgAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTFORFF0TlRjMk9DMDROelkzTFdOaU1XVXROVEJrWWpKaFlXWmhaRFUySWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAArwAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTNOVEl0TkRVek9TMDNPVFE0TFRaak9EVXRaalJoWm1RMk1XWmhaR1EySWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
        fum_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
        fum_df = pd.concat([fum_df1,fum_df2,fum_df3,fum_df4,fum_df5,fum_df6,fum_df7,fum_df8,fum_df9,fum_df10]).reset_index(drop=True)
        print('fum_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/reg/all/defensiveinterceptions/desc'
        int_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAGQAAABlACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUXhORFF0TkRFMk55MDVOVFV3TFRGa05UUXRNekUwWXpJNE56TXlPVFE0SWl3aU1qQXlNeUpkZlE9PQ=='
        int_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAMgAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUXlOVEl0TkdZM015MDVNVFUzTFRSaE16Y3RZMkkxWlRobFlXUTJNR1F4SWl3aU1qQXlNeUpkZlE9PQ=='
        int_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAASwAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUmhOR1l0TkdVeE1DMHlNVFV4TFRGalpqa3ROalkyTlRFMU1Ua3hZV0UxSWl3aU1qQXlNeUpkZlE9PQ=='
        int_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        int_df = pd.concat([int_df1,int_df2,int_df3,int_df4]).reset_index(drop=True)
        print('int_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/field-goals/'+year+'/reg/all/kickingfgmade/desc'
        fg_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/field-goals/'+year+'/REG/all/kickingfgmade/DESC?aftercursor=AAAAGQAAABhAOAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOQ0lzSWpNeU1EQTBZVFJtTFRVek1qQXRPRFEyTkMwMFptUmhMVFF3TnpFM1pXUTVOMlJoWlNJc0lqSXdNak1pWFgwPQ=='
        fg_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAMgAAACBAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUTBOREV0TlRZME1pMDROVGt5TFRrNU16WXRNRGM0T1RabU5UVTVNV05qSWl3aU1qQXlNeUpkZlE9PQ=='
        fg_df = pd.concat([fg_df1,fg_df2]).reset_index(drop=True)
        print('fum_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/'+year+'/reg/all/kickofftotal/desc'
        ko_df1 = Player_DF_Creator_NFL(url, lk_table_mascot) 
        url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/'+year+'/REG/all/kickofftotal/DESC?aftercursor=AAAAGQAAABdAUwAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNOaUlzSWpNeU1EQTFNelF4TFRSbE56a3ROakk1T1MwNE5USmxMV0l4TnpkbFpXVTVNamM0TUNJc0lqSXdNak1pWFgwPQ=='
        ko_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        ko_df = pd.concat([ko_df1,ko_df2]).reset_index(drop=True)
        print('ko_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/reg/all/kickreturnsaverageyards/desc'
        kor_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAGQAAABlAOQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOUzR3SWl3aU16SXdNRFE1TlRNdE5ERTFOaTB5TnpJeUxXSm1Nall0TmpJeE9ERXpOVEZoTWpJMElpd2lNakF5TXlKZGZRPT0='
        kor_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJANVR64UeuFDFleUp6WldGeVkyaEJablJsY2lJNld5SXlNUzR6TXlJc0lqTXlNREEwTWpSbUxUVTNNRFl0T0RZMk9DMWlORE01TFdFNU9UTmhZekJsT1dRMVpDSXNJakl3TWpNaVhYMD0='
        kor_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAASwAAAEtAMQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOeTR3SWl3aU16SXdNRFF4TkdNdE5HTXhNQzA0T1RreExUSTVOVFV0WWpWaU5qSTRPR001WVdabElpd2lNakF5TXlKZGZRPT0='
        kor_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAZAAAAGJAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNMakFpTENJek1qQXdOV0UwTVMwME16RXpMVE14T0RBdFltRXdNUzFoWlRneE1ETXpNVFJtWVRJaUxDSXlNREl6SWwxOQ=='
        kor_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        kor_df = pd.concat([kor_df1,kor_df2,kor_df3,kor_df4,kor_df5]).reset_index(drop=True)
        print('kor_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/punts/'+year+'/reg/all/puntingaverageyards/desc'
        punt_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://nfl.com/stats/player-stats/category/punts/'+year+'/REG/all/puntingaverageyards/DESC?aftercursor=AAAAGQAAABlARxrhR64UezFleUp6WldGeVkyaEJablJsY2lJNld5STBOaTR5TVNJc0lqTXlNREExTnpRNExUUTFOelV0TlRNMk5TMWxPVFF4TFRWaFpqUTJZMlV4WmpKa01TSXNJakl3TWpNaVhYMD0='
        punt_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        punt_df = pd.concat([punt_df1,punt_df2]).reset_index(drop=True)
        print('punt_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/reg/all/puntreturnsaverageyards/desc'
        puntr_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAGQAAABlAI4AAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVMamMxSWl3aU16SXdNRFEwTkRFdE5USXlOaTB4TXpRMkxUaG1ORFV0T0dRd1lXSTNOakU0WVRrNUlpd2lNakF5TXlKZGZRPT0='
        puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJAHZmZmZmZmjFleUp6WldGeVkyaEJablJsY2lJNld5STNMalFpTENJek1qQXdOVE0wT0MwME1URXdMVGMwTWpjdFpqTTBZUzFpWWpCaFlURmtPR1UxTlRZaUxDSXlNREl6SWwxOQ=='
        puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        puntr_df = pd.concat([puntr_df1,puntr_df2]).reset_index(drop=True)
        print('puntr_df Complete')
    else:
        url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/reg/all/passingyards/desc'
        qb_df = loop_urls(lk_table_mascot,url)
        #url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAZCAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOakVpTENJek1qQXdOVGswWmkwMU5URXlMVFEzTmpNdFlXSXlOQzFqTVdKa01EVXhaV1l3WldZaUxDSXlNREkwSWwxOQ=='
        #url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/REG/all/passingyards/DESC?aftercursor=AAAAGQAAABlAZCAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOakVpTENJek1qQXdOVGswWmkwMU5URXlMVFEzTmpNdFlXSXlOQzFqTVdKa01EVXhaV1l3WldZaUxDSXlNREkwSWwxOQ=='
        #qb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/passing/'+year+'/REG/all/passingyards/DESC?aftercursor=AAAAMgAAADJAgPgAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFORE1pTENJek1qQXdOR00wWmkwME16TTNMVFEwT0RJdE9UQTBZeTFoTkRkbU9HUm1NV1EwTVdJaUxDSXlNREl6SWwxOQ=='
        #qb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #qb_df = pd.concat([qb_df1,qb_df2]).reset_index(drop=True)
        print('qb_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/reg/all/rushingyards/desc'
        rb_df = loop_urls(lk_table_mascot,url,50)
        # url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAGQAAABlASAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBPQ0lzSWpNeU1EQTFORFF4TFRVNU5ETXRNVFl4T0Mxak1EZ3hMVFZrWkRaaU1tUXdZamd5T1NJc0lqSXdNalFpWFgwPQ=='
        # rb_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAMgAAADJAOgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlOaUlzSWpNeU1EQTBORFJtTFRVM016SXRPVGMxTVMxak1EaGpMVGd3TXpJNU1qbGxOak5sWWlJc0lqSXdNalFpWFgwPQ=='
        # rb_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAASwAAAEdALAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOQ0lzSWpNeU1EQTFNalJtTFRReU56RXROemN5TmkwNFkySm1MV1ZqT0dJMFl6WmlNVFl5TnlJc0lqSXdNalFpWFgwPQ=='
        # rb_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAZAAAAGNAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNJaXdpTXpJd01EUTNOR1l0TkRZeU1TMDVOak0yTFRjek5UUXRaREpsWWpZek5qVmtNalUzSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rb_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/rushing/'+year+'/REG/all/rushingyards/DESC?aftercursor=AAAAfQAAAHw_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EVXpORGd0TkRVME5TMDRPRGt6TFRSbE9HSXROVGN5TkRNd01tUmxNRGc0SWl3aU1qQXlOQ0pkZlE9PQ=='
        # rb_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # rb_df = pd.concat([rb_df1, rb_df2, rb_df3, rb_df4, rb_df5, rb_df6]).reset_index(drop=True)
        print('rb_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/reg/all/receivingreceptions/desc'
        rec_df = loop_urls(lk_table_mascot,url,50)
        # rec_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAGQAAABdAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EUTFOVFl0TkRFMU15MDBNekE1TFdJeVpXUXRObUk0TWpNelpqWm1aV0UxSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAMgAAAClAEAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBJaXdpTXpJd01EUmlORGt0TlRRek9DMDRNamt3TFdWbFpXUXRZemxqT1dOallUWXlaV014SWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAASwAAAEJACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUTBOR1l0TkRJeU1DMDNOalExTFRkbFpUY3RPVFJtTlRka00yVmxaRFJtSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAZAAAAGNARQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNaUlzSWpNeU1EQTBPRFE1TFRRM016Z3ROemM1TVMwNVpqZzVMV1ExTlRaak5HSTFPV0k1WVNJc0lqSXdNak1pWFgwPQ=='
        # rec_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAfQAAAGhAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUmhOR1l0TkRnd01DMHdNREUzTFdFeE9XRXRZVFUxTkdSbFpURXhOR1ZrSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAAlgAAAGhAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EVTNOREV0TlRJMk5TMDVOakV5TFRKbE5qZ3RaamxsTldZME0yRmpOVEkzSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAArwAAAJo_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTROREV0TlRJME9TMHpNVFl6TFdZNFpqVXROek5qTlRWbU9HRTFZekJrSWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/receiving/'+year+'/REG/all/receivingreceptions/DESC?aftercursor=AAAA4QAAAOAAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EUXhOR010TkdNd09TMDRNams1TFdZd01HWXRNamM0T1RVeE56UTJOamN5SWl3aU1qQXlOQ0pkZlE9PQ=='
        # rec_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # rec_df = pd.concat([rec_df1, rec_df2, rec_df3, rec_df4, rec_df5, rec_df6, rec_df7, rec_df8, rec_df9]).reset_index(drop=True)
        print('rec_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/reg/all/defensivecombinetackles/desc'
        tack_df = loop_urls(lk_table_mascot,url)
        # tack_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAGQAAABJAJAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNQzR3SWl3aU16SXdNRFV6TlRBdE5Ea3pNaTA1TmpJM0xXWmxPREl0WmpkbU9UY3lOR013TXpJMUlpd2lNakF5TkNKZGZRPT0='
        # tack_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAAMgAAAC5AIAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STRMakFpTENJek1qQXdORGcwT1MwMFl6RTJMVFE1T1RRdE4ySTVPUzFsT1RObFltSm1NbVE0TXpnaUxDSXlNREkwSWwxOQ=='
        # tack_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/tackles/'+year+'/REG/all/defensivecombinetackles/DESC?aftercursor=AAAASwAAADlAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNMakFpTENJek1qQXdOVE0wWkMwME9UWTRMVFV3TXpJdFpXRmtOUzAwWkRrMlpHTXhNVE0wWmpJaUxDSXlNREkwSWwxOQ=='
        # tack_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # tack_df = pd.concat([tack_df1,tack_df2,tack_df3,tack_df4]).reset_index(drop=True)
        print('tack_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/reg/all/defensiveforcedfumble/desc'
        fum_df = loop_urls(lk_table_mascot,url)
        # fum_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAGQAAABcAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EUXhORFF0TkRFMk55MDVOVFV3TFRGa05UUXRNekUwWXpJNE56TXlPVFE0SWl3aU1qQXlOQ0pkZlE9PQ=='
        # fum_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAMgAAABcAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EUXlOREV0TlRJM05pMHpNamd4TFRrd01qUXRaakV6TXpFMVlUazBNek16SWl3aU1qQXlOQ0pkZlE9PQ=='
        # fum_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAASwAAABcAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EUXlOR1l0TlRreU1pMDVNVFk0TFdFd01qQXROekl6WmpZellXWXdZMlUySWl3aU1qQXlOQ0pkZlE9PQ=='
        # fum_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAlgAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTFORFF0TlRjMk9DMDROelkzTFdOaU1XVXROVEJrWWpKaFlXWmhaRFUySWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAArwAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTNOVEl0TkRVek9TMDNPVFE0TFRaak9EVXRaalJoWm1RMk1XWmhaR1EySWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df6 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df7 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAAyAAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmhOR1l0TkRnek1pMHhPRFF6TFRobVltVXRPVEZsTjJGa016WmhPV1ppSWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df8 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df9 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/fumbles/'+year+'/REG/all/defensiveforcedfumble/DESC?aftercursor=AAAA4QAAAF8_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmtOR1l0TlRJM01DMDVOemd4TFdWa1lUSXRPRGxrWVdGbFpHSTBPR1kzSWl3aU1qQXlNeUpkZlE9PQ=='
        #fum_df10 = Player_DF_Creator_NFL(url, lk_table_mascot)
        # fum_df = pd.concat([fum_df1,fum_df2,fum_df3,fum_df4]).reset_index(drop=True)
        print('fum_df Complete')
        
        
        url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/reg/all/defensiveinterceptions/desc'
        int_df = loop_urls(lk_table_mascot,url)
        #int_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAGQAAABlACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUXhORFF0TkRFMk55MDVOVFV3TFRGa05UUXRNekUwWXpJNE56TXlPVFE0SWl3aU1qQXlNeUpkZlE9PQ=='
        #int_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAAMgAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUXlOVEl0TkdZM015MDVNVFUzTFRSaE16Y3RZMkkxWlRobFlXUTJNR1F4SWl3aU1qQXlNeUpkZlE9PQ=='
        #int_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/interceptions/'+year+'/REG/all/defensiveinterceptions/DESC?aftercursor=AAAASwAAACxAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUmhOR1l0TkdVeE1DMHlNVFV4TFRGalpqa3ROalkyTlRFMU1Ua3hZV0UxSWl3aU1qQXlNeUpkZlE9PQ=='
        #int_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #int_df = pd.concat([int_df1]).reset_index(drop=True)
        print('int_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/field-goals/'+year+'/reg/all/kickingfgmade/desc'
        fg_df = loop_urls(lk_table_mascot,url)
        #fg_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/field-goals/'+year+'/REG/all/kickingfgmade/DESC?aftercursor=AAAAGQAAABY_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUmlOR1l0TkdZd01TMHlPVFF5TFRnMU5EWXROMlU1TlRJeU5qZG1PREk1SWl3aU1qQXlOQ0pkZlE9PQ=='
        #fg_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #fg_df = pd.concat([fg_df1,fg_df2]).reset_index(drop=True)
        print('fg_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/'+year+'/reg/all/kickofftotal/desc'
        ko_df = loop_urls(lk_table_mascot,url)
        #ko_df1 = Player_DF_Creator_NFL(url, lk_table_mascot) 
        #url = 'https://www.nfl.com/stats/player-stats/category/kickoffs/'+year+'/REG/all/kickofftotal/DESC?aftercursor=AAAAGQAAABVAEAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBJaXdpTXpJd01EVTVOR1l0TlRJeE9DMDVNak14TFRSbU1EY3RZVGhqTmpFMU56Qm1abUl5SWl3aU1qQXlOQ0pkZlE9PQ=='
        #ko_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #ko_df = pd.concat([ko_df1,ko_df2]).reset_index(drop=True)
        print('ko_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/reg/all/kickreturnsaverageyards/desc'
        kor_df = loop_urls(lk_table_mascot,url)
        #kor_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAGQAAABdANgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlNaTR3SWl3aU16SXdNRFUzTkRFdE5UTTJNQzAwTXpJMUxUSmxOR1l0WWpFeFpEVmxaREkyTkRJM0lpd2lNakF5TkNKZGZRPT0='
        #kor_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJANVR64UeuFDFleUp6WldGeVkyaEJablJsY2lJNld5SXlNUzR6TXlJc0lqTXlNREEwTWpSbUxUVTNNRFl0T0RZMk9DMWlORE01TFdFNU9UTmhZekJsT1dRMVpDSXNJakl3TWpNaVhYMD0='
        #kor_df3 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAASwAAAEtAMQAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhOeTR3SWl3aU16SXdNRFF4TkdNdE5HTXhNQzA0T1RreExUSTVOVFV0WWpWaU5qSTRPR001WVdabElpd2lNakF5TXlKZGZRPT0='
        #kor_df4 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/kickoff-returns/'+year+'/REG/all/kickreturnsaverageyards/DESC?aftercursor=AAAAZAAAAGJAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNMakFpTENJek1qQXdOV0UwTVMwME16RXpMVE14T0RBdFltRXdNUzFoWlRneE1ETXpNVFJtWVRJaUxDSXlNREl6SWwxOQ=='
        #kor_df5 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #kor_df = pd.concat([kor_df1]).reset_index(drop=True)
        print('kor_df Complete')
        
        url = 'https://www.nfl.com/stats/player-stats/category/punts/'+year+'/reg/all/puntingaverageyards/desc'
        punt_df = loop_urls(lk_table_mascot,url)
        #punt_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://nfl.com/stats/player-stats/category/punts/'+year+'/REG/all/puntingaverageyards/DESC?aftercursor=AAAAGQAAABlARYAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBNeTR3SWl3aU16SXdNRFF5TkdZdE5UTTNOQzB6TXpVMUxUVmhPVEV0TkRnd1pHTmlNakpsTWpOaUlpd2lNakF5TkNKZGZRPT0='
        #punt_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #punt_df = pd.concat([punt_df1,punt_df2]).reset_index(drop=True)
        print('punt_df Complete')

        url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/reg/all/puntreturnsaverageyards/desc'
        puntr_df = loop_urls(lk_table_mascot,url)
        #puntr_df1 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAGQAAABcAAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdMakFpTENJek1qQXdOVGMwT1MwMFl6SXlMVEl4TXpFdFptVXhNUzA1TWpSbVpERXhNelU1Tm1ZaUxDSXlNREkwSWwxOQ=='
        #puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #url = 'https://www.nfl.com/stats/player-stats/category/punt-returns/'+year+'/REG/all/puntreturnsaverageyards/DESC?aftercursor=AAAAMgAAADJAHZmZmZmZmjFleUp6WldGeVkyaEJablJsY2lJNld5STNMalFpTENJek1qQXdOVE0wT0MwME1URXdMVGMwTWpjdFpqTTBZUzFpWWpCaFlURmtPR1UxTlRZaUxDSXlNREl6SWwxOQ=='
        #puntr_df2 = Player_DF_Creator_NFL(url, lk_table_mascot)
        #puntr_df = pd.concat([puntr_df1,puntr_df2]).reset_index(drop=True)
        print('puntr_df Complete')





    print('Complete')

    return qb_df, rb_df, rec_df, int_df, fg_df, ko_df, kor_df, punt_df, puntr_df, fum_df

def NFL_stats_off(lk_table_mascot, year):
    year = str(year)
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/'+year+'/reg/all'
    passing_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/rushing/'+year+'/reg/all'
    rushing_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/receiving/'+year+'/reg/all'
    receiving_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/scoring/'+year+'/reg/all'
    scoring_off_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/downs/'+year+'/reg/all'
    downs_off_df = DF_Creator(url, lk_table_mascot)
    print('teams offense complete')
    return passing_off_df, rushing_off_df, receiving_off_df, scoring_off_df, downs_off_df

def NFL_stats_def(lk_table_mascot, year):
    year = str(year)
    url = 'https://www.nfl.com/stats/team-stats/defense/passing/'+year+'/reg/all'
    passing_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/rushing/'+year+'/reg/all'
    rushing_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/receiving/'+year+'/reg/all'
    receiving_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/scoring/'+year+'/reg/all'
    scoring_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/tackles/'+year+'/reg/all'
    tackles_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/downs/'+year+'/reg/all'
    downs_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/fumbles/'+year+'/reg/all'
    fumbles_def_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/interceptions/'+year+'/reg/all'
    interception_def_df = DF_Creator(url, lk_table_mascot)
    print('teams defense complete')
    return passing_def_df, rushing_def_df, receiving_def_df, scoring_def_df, tackles_def_df, downs_def_df, fumbles_def_df, interception_def_df

def NFL_stats_st(lk_table_mascot, year):
    year = str(year)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/field-goals/'+year+'/reg/all'
    special_fg_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/scoring/'+year+'/reg/all'
    special_scoring_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/kickoffs/'+year+'/reg/all'
    special_kickoff_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/kickoff-returns/'+year+'/reg/all'
    special_kickoff_return_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/punts/'+year+'/reg/all'
    special_punting_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/special-teams/punt-returns/'+year+'/reg/all'
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

    url = 'https://www.nfl.com/stats/team-stats/defense/passing/2021/reg/all'
    passing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/rushing/2021/reg/all'
    rushing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/2021/reg/all'
    passing_of = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/rushing/2021/reg/all'
    rushing_of = DF_Creator(url, lk_table_mascot)
    print('Complete')

    return rush_df, rush_yd_per_gp_df, pass_df, rec_df_cbs, rec_rec_per_gp_df, kick_df1, score_df, passing_df, rushing_df, passing_of, rushing_of



if __name__ == '__main__':
    
    import PullRosters_OLD
    import utils
    
    
    
    
    week_list, lk_table_mascot, lk_table, CBS_URLs, NFL_URLs = utils.init()
    NFL_stats(lk_table_mascot, 2024)
    
    # standings_df = standings(lk_table)
    
    # (qb_df, rb_df, rec_df) = NFL_stats(lk_table_mascot)
    # (rush_df, rush_yd_per_gp_df, pass_df, rec_df_cbs, rec_rec_per_gp_df, kick_df1, score_df, passing_df, rushing_df, passing_of, rushing_of) = CBS_Stats(lk_table_mascot)
    
    # output = Output(standings_df, week_list)
