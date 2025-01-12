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

def SearchTable_NFL(soup,table,team):
    import utils
    
    table_headers=[]
    for x in soup.find_all('th'):
        data = x.text.strip()
        if data in table_headers:
            continue
        table_headers.append(data)
        
    table_headers.append('Team')

    final = []
    team_list=[]
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        row_list=[]
        if(columns != []):
            for i in range(0,len(columns)):
                data = columns[i].text.strip()
                data = utils.string_to_float(data)
                row_list.append(data)
            team = team.replace('-',' ')
            team = utils.capitalize_first_character(team)
            team = utils.capitalize_after_space(team)
            row_list.append(team)
        final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
    return df

def SearchTable_ProFootballArchives(soup,table):
    import utils
        

    table_headers = ['Team', 'Link']
    final = []
    for tr in soup.find_all('tr'):
        team_found = False
        if any(exclude in tr.text.strip().lower() for exclude in ['canadian', 'usfl', 'xfl']):
            break
        for value in tr.find_all('td'):   
            row_list=[] 
            if any(exc in value.text.strip().lower() for exc in ['season', 'playoff']):
                break
            else:
                team_found = True
        
    
            try:
                team_name = value.text.strip()
                if '*' in team_name:
                    team_name = team_name[:-1]
                row_list.append(team_name)
                if value.contents[0].attrs['href']:
                    row_list.append(value.contents[0].attrs['href'])
            except:
                pass
            if team_found == True:
                break
        if row_list != []:
            final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
    df.drop_duplicates(subset=['Team'],inplace=True)
    return df

def SearchTable_ProFootballArchives_Team(soup,table,team):
    import utils
    
    table_headers=[]
    for tr in table.find_all('tr'):
        if len(tr) > 1 and len(tr.find_all('th')) > 1:
            for x in tr.find_all('th'):
                data = x.text.strip()
                if data in table_headers:
                    continue
                table_headers.append(data)
            table_headers.append('Team')
            break
        
    final = []
    for row in table.find_all('tr'): 
        columns = row.find_all('td')
        row_list=[]
        if(columns != []):
            for i in range(0,len(columns)):
                data = columns[i].text.strip()
                data = utils.string_to_float(data)
                row_list.append(data)
            team = team.replace('-',' ')
            team = utils.capitalize_first_character(team)
            team = utils.capitalize_after_space(team)
            row_list.append(team)
        if row_list != []:
            final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
                
    return df

def SearchTable_CBS(soup,table,team):
    
    table_headers=[]
    for x in soup.find_all('th'):
        data = x.text.strip()
        if '\n' in data:
            data = data[:data.find('\n')]
        if '(' in data:
            end = find_nth(data, '(', 1)
            data=data[:end]
        if data in table_headers:
            continue
        table_headers.append(data)
        
    table_headers.append('Team')

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
                    start = find_nth(data, '\n', 2)
                    end = find_nth(data, '\n', 3)
                    data=data[start+len('\n'):end]
                if '.' in data and find_nth(data, '.', 1) < 2:
                    start = find_nth(data, ' ', 1)
                    end = find_nth(data, ' ', 2)
                    lastname_firstname=data[start+len(' '):end]
                    if find_nth_capital(lastname_firstname, 2) == -1:
                        start = find_nth(data, ' ', 1)
                        end = find_nth(data, ' ', 3)
                        lastname_firstname=data[start+len(' '):end]
                    end = find_nth_capital(lastname_firstname, 2)
                    if '-' in lastname_firstname or '.' in lastname_firstname or find_nth_capital(lastname_firstname, 3)!= -1:
                        end = find_nth_capital(lastname_firstname, 3)
                    lastname = lastname_firstname[:end]
                    firstname = lastname_firstname[end:]
                    data = firstname+' '+lastname
                if ' ' in data:
                    data = re.sub(r"^\s+", '', data)
                if '(' in data:
                    end = find_nth(data, '(', 1)
                    data=data[:end]
                row_list.append(data)
            end = find_nth(team, '/', 1)
            row_list.append(team[:end])
        final.append(row_list)
    df = pd.DataFrame(final,columns = table_headers)
    return df


def SwitchTables(table):
    next_table = table.find_next_sibling('table', class_='TableBase-table')
    return next_table

def PullTeam_CBS(url,team):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))
    
    #  Looking for the table with the classes 'wikitable' and 'sortable'
    database_df_final = pd.DataFrame()
    table = soup.find('table', class_='TableBase-table')
    for wrapper in soup.find_all(class_='TableBaseWrapper'):

        for table in wrapper.find_all('table', class_='TableBase-table'):
            if table:

                df = SearchTable(soup,table,team)
                database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
            else:
                print(f"No table found for '{wrapper.text}'")
    # for i in range(1,len(soup.find_all('h4'))):
        
    #     if i != 1:
    #         table = SwitchTables(table)
        
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    
    # for table in soup.find_all('table'):
    #     table = soup.find('table', class_='TableBase-table')
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    return database_df_final

def PullTeam_NFL(url,team):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))
    
    #  Looking for the table with the classes 'wikitable' and 'sortable'
    database_df_final = pd.DataFrame()
    #table = soup.find('table', class_='d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-table--sortable')
    for table in soup.find_all('table'):
        df = SearchTable_NFL(soup,table,team)
        database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)

    # for i in range(1,len(soup.find_all('h4'))):
        
    #     if i != 1:
    #         table = SwitchTables(table)
        
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    
    # for table in soup.find_all('table'):
    #     table = soup.find('table', class_='TableBase-table')
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    return database_df_final



def PullTeam_ProFootballArchives(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('Classes of each table:')
    # for table in soup.find_all('table'):
    #     print(table.get('class'))
    
    #  Looking for the table with the classes 'wikitable' and 'sortable'
    database_df_final = pd.DataFrame()
    #table = soup.find('table', class_='d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-table--sortable')
    for table in soup.find_all('table'):
        database_df_final = pd.DataFrame()
        df = SearchTable_ProFootballArchives(soup,table)
        for i in range(len(df)):
            team_name = df.iloc[i,0]
            link = df.iloc[i,1]
            url = 'https://www.profootballarchives.com/'+link
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            # print('Classes of each table:')
            # for table in soup.find_all('table'):
            #     print(table.get('class'))
            
            #  Looking for the table with the classes 'wikitable' and 'sortable'
            first = True
            for table in soup.find_all(class_ = 'stats'):
                if first == True:
                    first = False
                    continue
                df_archive = SearchTable_ProFootballArchives_Team(soup,table,team_name)
                if len(df_archive) > 0:
                    break
            database_df_final = pd.concat([database_df_final,df_archive]).reset_index(drop=True)
            print(f'{team_name} complete')
            #table = soup.find('table', class_='d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-table--sortable')
        break

    # for i in range(1,len(soup.find_all('h4'))):
        
    #     if i != 1:
    #         table = SwitchTables(table)
        
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    
    # for table in soup.find_all('table'):
    #     table = soup.find('table', class_='TableBase-table')
    #     df = SearchTable(soup,table,team)
    #     database_df_final = pd.concat([database_df_final,df]).reset_index(drop=True)
    
    return database_df_final