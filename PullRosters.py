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

def SearchTable(soup,table,team):
    
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
                if '.' in data:
                    start = find_nth(data, ' ', 1)
                    end = find_nth(data, ' ', 2)
                    lastname_firstname=data[start+len(' '):end]
                    end = find_nth_capital(lastname_firstname, 2)
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

def PullTeam(url,team):
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