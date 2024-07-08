from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import os


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

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Schedule.csv')
    schedule = pd.read_csv(filename,header=0,index_col=0)
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

if __name__ == '__main__':
    week_list, lk_table_mascot, lk_table = init()
    standings_df = standings(lk_table)

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
    rec_df = pd.concat([rec_df1,rec_df2]).reset_index(drop=True)
    rec_df['REC/GP'] = rec_df['REC'].astype(int) / rec_df['GP'].astype(int)
    rec_rec_per_gp_df = rec_df.sort_values(by='REC/GP', ascending=False).reset_index(drop=True)


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
    output = Output(standings_df)
    print('Complete')

    rush_df = rush_df[0:10]
    top_ten = rush_df.sort_values('YDS/G', ascending=False)
    plt.bar(top_ten['Player'], top_ten['YDS/G'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Rushing Yards Per Game')
    plt.ylabel('Yards Per Game')
    plt.ylim(50, 100)
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2024/plots/Top_10_Rushing_Yards_Per_Game.png', dpi=450)
    plt.close()

    print(passing_of)
    passing_plays_forty = passing_of.sort_values('40+', ascending=False)
    plt.bar(passing_of.index, passing_of['40+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 40+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2024/plots/40yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_plays_twenty = passing_of.sort_values('20+', ascending=False)
    plt.bar(passing_of.index, passing_of['20+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 20+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2024/plots/20yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_top_ten = pass_df1.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(passing_top_ten['Player'], passing_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(220, 350)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Passing Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2024/plots/Top_10_Passing_Yards_Per_Game.png', dpi=450)
    plt.close()

    rec_top_ten = rec_df.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(rec_top_ten['Player'], rec_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(50, 100)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Recieving Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2024/plots/Top_10_Recieving_Yards_Per_Game.png', dpi=450)
