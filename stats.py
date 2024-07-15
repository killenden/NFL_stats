
import utils
import pandas as pd
import os
import PullFromDatabase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors as mcolors

def export_stats(filename, df):
    if UpdatePlayerDatabase.check_csv_file(filename+'.csv') == False:
        current_dir = os.getcwd()  # Get current working directory
        file_path = os.path.join(current_dir, filename+'.csv')  # Create file path
        os.remove(file_path)


        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, filename)  # Create file path
        df.to_csv(file_path+'.csv', index=False)
    else:
        df = pd.read_csv(filename.endswith('.csv'))

def plots(): 
    rush_df = rush_df[0:10]
    top_ten = rush_df.sort_values('YDS/G', ascending=False)
    plt.bar(top_ten['Player'], top_ten['YDS/G'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Rushing Yards Per Game')
    plt.ylabel('Yards Per Game')
    plt.ylim(50, 100)
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Rushing_Yards_Per_Game.png', dpi=450)
    plt.close()

    print(passing_of)
    passing_plays_forty = passing_of.sort_values('40+', ascending=False)
    plt.bar(passing_of.index, passing_of['40+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 40+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/40yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_plays_twenty = passing_of.sort_values('20+', ascending=False)
    plt.bar(passing_of.index, passing_of['20+'].astype(float), zorder=2)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Passing Plays of 20+ Yards')
    plt.ylabel('Frequency')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/20yrd_passing_plays.png', dpi=450)
    plt.close()

    passing_top_ten = pass_df1.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(passing_top_ten['Player'], passing_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(220, 350)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Passing Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Passing_Yards_Per_Game.png', dpi=450)
    plt.close()

    rec_top_ten = rec_df.sort_values('YDS/G', ascending=False).head(10)
    plt.bar(rec_top_ten['Player'], rec_top_ten['YDS/G'].astype(float), zorder=2)
    plt.ylim(50, 100)
    plt.xticks(rotation=45)
    plt.title('NFL 2023: Top 10 Recieving Yards Per Game')
    plt.ylabel('Yards')
    plt.grid(axis='y', zorder=1, color='black')
    plt.tight_layout()
    plt.savefig(r'2023/plots/Top_10_Recieving_Yards_Per_Game.png', dpi=450)

    team_list = passing_df.index.tolist()
    rushing_df['Team_Name'] = rushing_df.index
    rushing_first_rate = rushing_df['Rush 1st%'].astype(float)
    passing_df['Team_Name'] = passing_df.index
    passing_first_rate = passing_df['1st%'].astype(float)

    first_down_df = pd.merge(rushing_df[['Team_Name', 'Rush 1st%']], passing_df[['Team_Name', '1st%']], on='Team_Name')

    print(first_down_df)

    def get_team_logo(team_abbr):
        current_dir = os.getcwd()
        logo_dir = os.path.join(current_dir,'logos')
        file_path = os.path.join(logo_dir,team_abbr+'.png')
        return file_path

    #Convert columns to float
    first_down_df['Rush 1st%'] = first_down_df['Rush 1st%'].astype('float')
    first_down_df['1st%'] = first_down_df['1st%'].astype('float')

    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(first_down_df['Team_Name']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (first_down_df['Rush 1st%'][i], first_down_df['1st%'][i]), frameon=False)
        ax.add_artist(ab)

    # Set labels and title
    ax.set_xlabel('Rush 1st%')
    ax.set_ylabel('1st%')
    ax.set_title('Scatter Plot of Rush 1st% vs 1st% with Team Logos')

    # Adjust plot limits
    plt.xlim(first_down_df['Rush 1st%'].min() - 1, first_down_df['Rush 1st%'].max() + 1)
    plt.ylim(first_down_df['1st%'].min() - 1, first_down_df['1st%'].max() + 1)
    plt.savefig('logos.png', dpi=450)
    plt.show()
    #plt.close()
    
def get_team_logo(team_abbr):
    current_dir = os.getcwd()
    logo_dir = os.path.join(current_dir,'logos')
    file_path = os.path.join(logo_dir,team_abbr+'.png')
    return file_path

def Team_Attempts(db_name):
    df = PullFromDatabase.team_off_plays(db_name)

    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Rush_Att'][i], df['Pass_Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Rush_Att']).mean()
    y_mean = (df['Pass_Att']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    # Set labels and title
    ax.set_xlabel('Rush Att')
    ax.set_ylabel('Pass Att')
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim(df['Rush_Att'].min() - 1, df['Rush_Att'].max() + 1)
    plt.ylim(df['Pass_Att'].min() - 1, df['Pass_Att'].max() + 1)
    plt.savefig('logos.png', dpi=450)
    plt.show()
    
def Team_Attempts_Pct(db_name):
    df = PullFromDatabase.team_off_plays(db_name)
    
    total_att = []
    for i in range(len(df)):
        total_att.append(df['Rush_Att'].iloc[i] + df['Pass_Att'].iloc[i])
        
    df['Tot_Att'] = total_att
    
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Rush_Att'][i]/df['Tot_Att'][i], df['Pass_Att'][i]/df['Tot_Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Rush_Att']/df['Tot_Att']).mean()
    y_mean = (df['Pass_Att']/df['Tot_Att']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    # Set labels and title
    ax.set_xlabel('Rush Att')
    ax.set_ylabel('Pass Att')
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Rush_Att']/df['Tot_Att']).min() - 0.025, (df['Rush_Att']/df['Tot_Att']).max() + 0.025)
    plt.ylim((df['Pass_Att']/df['Tot_Att']).min() - 0.025, (df['Pass_Att']/df['Tot_Att']).max() + 0.025)
    plt.savefig('logos.png', dpi=450)
    plt.show()

def Team_Attempts_Both(db_name):
    df = PullFromDatabase.team_both_plays(db_name)
    
    total_off_att = []
    total_def_att = []
    for i in range(len(df)):
        total_off_att.append(df['Rush_Off_Att'].iloc[i] + df['Pass_Off_Att'].iloc[i])
        
    for i in range(len(df)):
        total_def_att.append(df['Rush_Def_Att'].iloc[i] + df['Pass_Def_Att'].iloc[i])
        
    df['Tot_Off_Att'] = total_off_att
    df['Tot_Def_Att'] = total_def_att
    df['Tot_Att'] = df['Tot_Off_Att'] + df['Tot_Def_Att']
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Tot_Def_Att'][i], df['Tot_Off_Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Tot_Def_Att']).mean()
    y_mean = (df['Tot_Off_Att']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    # Set labels and title
    ax.set_xlabel('Def %')
    ax.set_ylabel('Off %')
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Tot_Def_Att']).min() - 0.025, (df['Tot_Off_Att']).max() + 0.025)
    plt.ylim((df['Tot_Off_Att']).min() - 0.025, (df['Tot_Off_Att']).max() + 0.025)
    plt.savefig('logos.png', dpi=450)
    plt.show()


def Team_Attempts_Both_Pct(db_name):
    df = PullFromDatabase.team_both_plays(db_name)
    
    total_off_att = []
    total_def_att = []
    for i in range(len(df)):
        total_off_att.append(df['Rush_Off_Att'].iloc[i] + df['Pass_Off_Att'].iloc[i])
        
    for i in range(len(df)):
        total_def_att.append(df['Rush_Def_Att'].iloc[i] + df['Pass_Def_Att'].iloc[i])
        
    df['Tot_Off_Att'] = total_off_att
    df['Tot_Def_Att'] = total_def_att
    df['Tot_Att'] = df['Tot_Off_Att'] + df['Tot_Def_Att']
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Tot_Def_Att'][i]/df['Tot_Att'][i], df['Tot_Off_Att'][i]/df['Tot_Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Tot_Def_Att']/df['Tot_Att']).mean()
    y_mean = (df['Tot_Off_Att']/df['Tot_Att']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    # Set labels and title
    ax.set_xlabel('Def %')
    ax.set_ylabel('Off %')
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Tot_Def_Att']/df['Tot_Att']).min() - 0.025, (df['Tot_Off_Att']/df['Tot_Att']).max() + 0.025)
    plt.ylim((df['Tot_Off_Att']/df['Tot_Att']).min() - 0.025, (df['Tot_Off_Att']/df['Tot_Att']).max() + 0.025)
    plt.savefig('logos.png', dpi=450)
    plt.show()
    
def Target_Share(db_name):
    df = PullFromDatabase.team_off_target_share_plays(db_name)
    
        
    df['Tgt_Share'] = df['Tgts'] / df['Pass_Off_Att']
    
    df = df[df['Tgt_Share'] > df['Tgt_Share'].mean()]
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for index, row in df.iterrows():
        plt.text(row['Pass_Off_Att'], row['Tgt_Share'], row['Player'], fontsize=9, ha='right', weight = 'bold', family = 'cursive')
        
    ax.scatter(df['Pass_Off_Att'], df['Tgt_Share'])

    x_mean = (df['Pass_Off_Att']).mean()
    y_mean = (df['Tgt_Share']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    # Set labels and title
    ax.set_xlabel('Total Team Passing Attempts')
    ax.set_ylabel('Target Share')
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Pass_Off_Att']).min() - 10, (df['Pass_Off_Att']).max() + 10)
    plt.ylim((df['Tgt_Share']).min() - 0.0125, (df['Tgt_Share']).max() + 0.0125)
    plt.savefig('logos.png', dpi=450)
    plt.show()



if __name__ == '__main__':
    year = 2021
    db_name = rf'database\{year}_database.db'
    Target_Share(db_name)
    
    