from bs4 import BeautifulSoup
import requests
import pandas as pd

def init():
    lk_table = {'Arizona Cardinals': 'ARI',
                'Atlanta Falcons': 'ATL',
                'Baltimore Ravens': 'BAL',
                'Buffalo Bills': 'BUF',
                'Carolina Panthers': 'CAR',
                'Chicago Bears': 'CHI',
                'Cincinnati Bengals': 'CIN',
                'Cleveland Browns': 'CLE',
                'Dallas Cowboys': 'DAL',
                'Denver Broncos': 'DEN',
                'Detroit Lions': 'DET',
                'Green Bay Packers': 'GB',
                'Houston Texans': 'HOU',
                'Indianapolis Colts': 'IND',
                'Jacksonville Jaguars': 'JAX',
                'Kansas City Chiefs': 'KC',
                'Las Vegas Raiders': 'LV',
                'Los Angeles Chargers': 'LAC',
                'Los Angeles Rams': 'LAR',
                'Miami Dolphins': 'MIA',
                'Minnesota Vikings': 'MIN',
                'New England Patriots': 'NE',
                'New Orleans Saints': 'NO',
                'New York Giants': 'NYG',
                'New York Jets': 'NYJ',
                'Philadelphia Eagles': 'PHI',
                'Pittsburgh Steelers': 'PIT',
                'San Francisco 49ers': 'SF',
                'Seattle Seahawks': 'SEA',
                'Tampa Bay Buccaneers': 'TB',
                'Tennessee Titans': 'TEN',
                'Washington Commanders': 'WSH'}

    lk_table_mascot = {'Cardinals': 'ARI',
                'Falcons': 'ATL',
                'Ravens': 'BAL',
                'Bills': 'BUF',
                'Panthers': 'CAR',
                'Bears': 'CHI',
                'Bengals': 'CIN',
                'Browns': 'CLE',
                'Cowboys': 'DAL',
                'Broncos': 'DEN',
                'Lions': 'DET',
                'Packers': 'GB',
                'Texans': 'HOU',
                'Colts': 'IND',
                'Jaguars': 'JAX',
                'Chiefs': 'KC',
                'Raiders': 'LV',
                'Chargers': 'LAC',
                'Rams': 'LAR',
                'Dolphins': 'MIA',
                'Vikings': 'MIN',
                'Patriots': 'NE',
                'Saints': 'NO',
                'Giants': 'NYG',
                'Jets': 'NYJ',
                'Eagles': 'PHI',
                'Steelers': 'PIT',
                '49ers': 'SF',
                'Seahawks': 'SEA',
                'Buccaneers': 'TB',
                'Titans': 'TEN',
                'Commanders': 'WSH'}


    schedule = pd.read_csv('Schedule.csv',header=0,index_col=0)
    week = 8
    week_list=[]
    for i in range(0,len(schedule)):
        week_list.append(schedule.iloc[i,week-1])
    return week_list, lk_table_mascot, lk_table


def Output(standings_df):
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


if __name__ == '__main__':
    week_list, lk_table_mascot, lk_table = init()
    standings_df = standings(lk_table)
    url = 'https://www.nfl.com/stats/team-stats/defense/passing/2023/reg/all'
    passing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/defense/rushing/2023/reg/all'
    rushing_df = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/passing/2023/reg/all'
    passing_of = DF_Creator(url, lk_table_mascot)
    url = 'https://www.nfl.com/stats/team-stats/offense/rushing/2023/reg/all'
    rushing_of = DF_Creator(url, lk_table_mascot)
    output = Output(standings_df)