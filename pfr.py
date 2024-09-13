import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from PIL import Image
from io import BytesIO
import os

def player_gamelog(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table_headers = []
    final = []
    for table in soup.find_all('table', id='stats'):
        for x in table.thead.find_all('tr'):
            if x.find(class_='over_header'):
                continue
            else:
                for y in x.find_all('th'):
                    table_headers.append(y['data-stat'].strip())
        for row in table.tbody.find_all('tr'):
            row_list = []
            columns = row.find_all('th')
            if columns != []:
                for i in range(0, len(columns)):
                    data = columns[i].text.strip()
            row_list.append(data)
            columns = row.find_all('td')
            if columns != []:
                for i in range(0, len(columns)):
                    data = columns[i].text.strip()
                    if '\n' in columns[i].text.strip():
                        data = data[:data.find('\n')]
                    if data == '':
                        data = np.nan
                    row_list.append(data)
            final.append(row_list)
    df = pd.DataFrame(final, columns=table_headers)

    return df

# # Example usage
# url = 'https://www.pro-football-reference.com/players/L/LambCe00/gamelog/2023/'
# df2 = player_gamelog(url)
# print(df2)

# fig, ax = plt.subplots(figsize=(12, 9))

# plt.plot(df2['week_num'].astype(float), df2['off_pct'].str.replace('%', '').astype(float), label='Offensive Percentage')
# #plt.show()
# plt.close()

# fig, ax = plt.subplots(figsize=(12, 9))
# plt.plot(df2['week_num'].astype(float), df2['off_pct'].str.replace('%', '').astype(float), label='Offensive Percentage', linewidth=2)
# plt.xticks(np.arange(1, 19, 1))
# plt.xlabel('Week Number')
# plt.ylabel('Offensive Snap Percentage')
# plt.ylim(60, 101)
# plt.xlim(1, 18)
# ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')
# plt.title('CeeDee Lamb 2023 Offensive Snap Percentage')
# plt.close()

def plot_offensive_snap_percentage_and_targets(df2):
    # Initial plot setup
    fig, ax1 = plt.subplots(figsize=(12, 9))

    # Plotting the first data series (offensive percentage)
    ax1.plot(df2['week_num'].astype(float), df2['off_pct'].str.replace('%', '').astype(float), label='Snap %', linewidth=2)
    ax1.set_xlabel('Week Number', fontsize=12)
    ax1.set_ylabel('Offensive Snap Percentage', fontsize=12)
    ax1.tick_params(axis='y')
    ax1.set_ylim(60, 100)
    ax1.set_xlim(1, 18)
    ax1.grid(True, which='both', axis='x', linewidth=0.5, linestyle='--')

    # Fetch and load the image
    url = 'https://www.pro-football-reference.com/req/20230307/images/headshots/LambCe00_2023.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    imagebox = OffsetImage(img, zoom=0.5)  # Adjust zoom as necessary
    ab = AnnotationBbox(imagebox, (0.05, 0.90), frameon=False, xycoords='axes fraction')  # Adjust placement
    ax1.add_artist(ab)

    # Create a second y-axis for the 'tgt' data
    ax2 = ax1.twinx()
    ax2.plot(df2['week_num'].astype(float), df2['targets'].astype(float), label='Targets', color='tab:red', linewidth=2)
    ax2.set_ylabel('Targets', fontsize=12)
    ax2.tick_params(axis='y')
    ax2.set_ylim(4, 18)

    # Adding title and legend
    plt.title('CeeDee Lamb 2023 Offensive Snap Percentage and Targets', fontsize=16, fontweight='bold')
    fig.tight_layout()  # Adjust layout to make room for the second y-axis

    # To create a single legend for both plots, you can manually define the legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='lower right')

    #plt.show()
    plt.close()

def test():
    url = 'https://www.pro-football-reference.com/years/2023/receiving_advanced.htm#advanced_receiving'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    table_headers = []
    final = []
    for table in soup.find_all('table', id='advanced_receiving'):
        for x in table.thead.find_all('tr'):
            for y in x.find_all('th'):
                table_headers.append(y['data-stat'].strip())
        for row in table.tbody.find_all('tr'):
            row_list = []
            columns = row.find_all('th')
            if columns != []:
                for i in range(0, len(columns)):
                    data = columns[i].text.strip()
            row_list.append(data)
            columns = row.find_all('td')
            if columns != []:
                for i in range(0, len(columns)):
                    data = columns[i].text.strip()
                    if '\n' in columns[i].text.strip():
                        data = data[:data.find('\n')]
                    if data == '':
                        data = np.nan
                    row_list.append(data)
            final.append(row_list)
    df = pd.DataFrame(final, columns=table_headers)
    print(df)

if __name__ == '__main__':
    test()
