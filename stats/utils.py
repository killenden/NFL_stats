def init():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import re
    import matplotlib.pyplot as plt
    import os
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

    CBS_URLs = ['ARI/arizona-cardinals',
                'ATL/atlanta-falcons',
                'BAL/baltimore-ravens',
                'BUF/buffalo-bills',
                'CAR/carolina-panthers',
                'CHI/chicago-bears',
                'CIN/cincinnati-bengals',
                'CLE/cleveland-browns',
                'DAL/dallas-cowboys',
                'DEN/denver-broncos',
                'DET/detroit-lions',
                'GB/green-bay-packers',
                'HOU/houston-texans',
                'IND/indianapolis-colts',
                'JAC/jacksonville-jaguars',
                'KC/kansas-city-chiefs',
                'LV/las-vegas-raiders',
                'LAC/los-angeles-chargers',
                'LAR/los-angeles-rams',
                'MIA/miami-dolphins',
                'MIN/minnesota-vikings',
                'NE/new-england-patriots',
                'NO/new-orleans-saints',
                'NYG/new-york-giants',
                'NYJ/new-york-jets',
                'PHI/philadelphia-eagles',
                'PIT/pittsburgh-steelers',
                'SF/san-francisco-49ers',
                'SEA/seattle-seahawks',
                'TB/tampa-bay-buccaneers',
                'TEN/tennessee-titans',
                'WAS/washington-commanders']
    
    NFL_URLs = ['arizona-cardinals',
                'atlanta-falcons',
                'baltimore-ravens',
                'buffalo-bills',
                'carolina-panthers',
                'chicago-bears',
                'cincinnati-bengals',
                'cleveland-browns',
                'dallas-cowboys',
                'denver-broncos',
                'detroit-lions',
                'green-bay-packers',
                'houston-texans',
                'indianapolis-colts',
                'jacksonville-jaguars',
                'kansas-city-chiefs',
                'las-vegas-raiders',
                'los-angeles-chargers',
                'los-angeles-rams',
                'miami-dolphins',
                'minnesota-vikings',
                'new-england-patriots',
                'new-orleans-saints',
                'new-york-giants',
                'new-york-jets',
                'philadelphia-eagles',
                'pittsburgh-steelers',
                'san-francisco-49ers',
                'seattle-seahawks',
                'tampa-bay-buccaneers',
                'tennessee-titans',
                'washington-commanders']

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Schedule.csv')
    schedule = pd.read_csv(filename,header=0,index_col=0)
    week = 8
    week_list=[]
    for i in range(0,len(schedule)):
        week_list.append(schedule.iloc[i,week-1])
    return week_list, lk_table_mascot, lk_table, CBS_URLs, NFL_URLs

def capitalize_after_space(input_string):
    result = []
    capitalize_next = False

    
    for char in input_string:
        if capitalize_next and char.isalpha():
            result.append(char.upper())
            capitalize_next = False
        else:
            result.append(char)
        
        if char == ' ':
            capitalize_next = True
        elif result[-1] != ' ':
            capitalize_next = False

    
    return ''.join(result)

def capitalize_first_character(input_string):
    if not input_string:
        return input_string

    return input_string[0].upper() + input_string[1:]

    
def string_to_float(string_num):
    try:
        string_num = int(string_num)
    except:
        try:
            string_num = float(string_num)
        except:
            pass
    return string_num

