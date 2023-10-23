from bs4 import BeautifulSoup
import requests
import pandas as pd



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
print(df1.sort_values(by='PCT', ascending=False))








url = 'https://www.nfl.com/stats/team-stats/defense/passing/2023/reg/all'
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

print(df.sort_values(by='Cmp %', ascending=False))










