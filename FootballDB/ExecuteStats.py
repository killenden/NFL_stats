
import pandas as pd
import os
import PullFromDatabase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../FootballDB')))
import PullFromDatabase
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Sleeper')))
import SleeperInfo

def get_team_logo(team_abbr):
    current_dir = os.getcwd()
    logo_dir = os.path.join(current_dir,'logos')
    file_path = os.path.join(logo_dir,team_abbr+'.png')
    return file_path

def save_fig(year, plot_name):
    current_directory = os.getcwd()
    # Ensure the plots directory exists
    plots_dir = os.path.join(current_directory, f'{year}/plots')
    os.makedirs(plots_dir, exist_ok=True)
    # Change the current working directory to the plots directory
    os.chdir(plots_dir)
    plt.savefig(f'{plot_name}.png', dpi=450)
    #change back
    os.chdir(current_directory)


def Team_RushAtt_PassAtt_Off(db_name, weeks, year):
    pass_df = PullFromDatabase.team_off_passing(db_name)
    rush_df = PullFromDatabase.team_off_rushing(db_name)
    df = pd.merge(pass_df, rush_df, on='team_name')
    df.drop('shortname_y', axis=1, inplace=True)
    df.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Rush Att'][i], df['Pass Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Rush Att']).mean()
    y_mean = (df['Pass Att']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    # Set labels and title
    ax.set_xlabel('Rush Att', fontsize=12)
    ax.set_ylabel('Pass Att', fontsize=12)
    ax.set_title(f'{year} Week {weeks}: Rush Att vs Pass Att', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim(df['Rush Att'].min() - (df['Rush Att'].min()/weeks)/2, df['Rush Att'].max() + (df['Rush Att'].max()/weeks)/2)
    plt.ylim(df['Pass Att'].min() - (df['Pass Att'].min()/weeks)/2, df['Pass Att'].max() + (df['Pass Att'].max()/weeks)/2)
    
    save_fig(year, f'Team_RushAtt_PassAtt_Off.png')
    plt.show()
    print('Team_RushAtt_PassAtt_Off Completed')
    
def Team_RushAtt_PassAtt_Off_Linearized(db_name, weeks, year):
    pass_df = PullFromDatabase.team_off_passing(db_name)
    rush_df = PullFromDatabase.team_off_rushing(db_name)
    df = pd.merge(pass_df, rush_df, on='team_name')
    df.drop('shortname_y', axis=1, inplace=True)
    df.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    
    total_att = []
    for i in range(len(df)):
        total_att.append(df['Rush Att'].iloc[i] + df['Pass Att'].iloc[i])
        
    df['Tot Att'] = total_att
    
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Rush Att'][i]/df['Tot Att'][i], df['Pass Att'][i]/df['Tot Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Rush Att']/df['Tot Att']).mean()
    y_mean = (df['Pass Att']/df['Tot Att']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    # Set labels and title
    ax.set_xlabel('Rush Att', fontsize=12)
    ax.set_ylabel('Pass Att', fontsize=12)
    ax.set_title(f'{year} Week {weeks}: Rush Att vs Pass Att Linearized', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Rush Att']/df['Tot Att']).min() - 0.025, (df['Rush Att']/df['Tot Att']).max() + 0.025)
    plt.ylim((df['Pass Att']/df['Tot Att']).min() - 0.025, (df['Pass Att']/df['Tot Att']).max() + 0.025)
    save_fig(year, f'Team_RushAtt_PassAtt_Off_Linearized.png')
    plt.show()
    print('Team_RushAtt_PassAtt_Off_Linearized Completed')

def Team_RushAtt_PassAtt_Both(db_name, weeks, year):
    pass_df = PullFromDatabase.team_off_passing(db_name)
    rush_df = PullFromDatabase.team_off_rushing(db_name)
    df1 = pd.merge(pass_df, rush_df, on='team_name')
    df1.drop('shortname_y', axis=1, inplace=True)
    df1.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    for col in df1.columns:
        if col != 'team_name' and col != 'shortname':
            df1.rename(columns={col: 'Off '+col}, inplace=True)
    
    pass_df = PullFromDatabase.team_def_passing(db_name)
    rush_df = PullFromDatabase.team_def_rushing(db_name)
    df2 = pd.merge(pass_df, rush_df, on='team_name')
    df2.drop('shortname_y', axis=1, inplace=True)
    df2.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    for col in df2.columns:
        if col != 'team_name' and col != 'shortname':
            df2.rename(columns={col: 'Def '+col}, inplace=True)
        
    df = pd.merge(df1, df2, on='team_name')
    df.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    
    total_off_att = []
    total_def_att = []
    for i in range(len(df)):
        total_off_att.append(df['Off Rush Att'].iloc[i] + df['Off Pass Att'].iloc[i])
        
    for i in range(len(df)):
        total_def_att.append(df['Def Rush Att'].iloc[i] + df['Def Pass Att'].iloc[i])
        
    df['Off Tot Att'] = total_off_att
    df['Def Tot Att'] = total_def_att
    df['Tot Att'] = df['Off Tot Att'] + df['Def Tot Att']
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Def Tot Att'][i], df['Off Tot Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Def Tot Att']).mean()
    y_mean = (df['Off Tot Att']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    # Set labels and title
    ax.set_xlabel('Def Tot Att', fontsize=12)
    ax.set_ylabel('Off Tot Att', fontsize=12)
    ax.set_title(f'{year} Week {weeks}: Defense Att vs Offense Att', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Def Tot Att']).min() - (df['Def Tot Att']).min()/weeks/2, (df['Def Tot Att']).max() + (df['Def Tot Att']).max()/weeks/2)
    plt.ylim((df['Off Tot Att']).min() - (df['Off Tot Att']).min()/weeks/2, (df['Off Tot Att']).max() + (df['Off Tot Att']).max()/weeks/2)
    save_fig(year, f'Team_RushAtt_PassAtt_Both.png')
    plt.show()
    print('Team_RushAtt_PassAtt_Both Completed')


def Team_RushAtt_PassAtt_Both_Linearized(db_name, weeks, year):
    pass_df = PullFromDatabase.team_off_passing(db_name)
    rush_df = PullFromDatabase.team_off_rushing(db_name)
    df1 = pd.merge(pass_df, rush_df, on='team_name')
    df1.drop('shortname_y', axis=1, inplace=True)
    df1.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    for col in df1.columns:
        if col != 'team_name' and col != 'shortname':
            df1.rename(columns={col: 'Off '+col}, inplace=True)
    
    pass_df = PullFromDatabase.team_def_passing(db_name)
    rush_df = PullFromDatabase.team_def_rushing(db_name)
    df2 = pd.merge(pass_df, rush_df, on='team_name')
    df2.drop('shortname_y', axis=1, inplace=True)
    df2.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    for col in df2.columns:
        if col != 'team_name' and col != 'shortname':
            df2.rename(columns={col: 'Def '+col}, inplace=True)
        
    df = pd.merge(df1, df2, on='team_name')
    df.rename(columns={'shortname_x': 'shortname'}, inplace=True)
    
    total_off_att = []
    total_def_att = []
    for i in range(len(df)):
        total_off_att.append(df['Off Rush Att'].iloc[i] + df['Off Pass Att'].iloc[i])
        
    for i in range(len(df)):
        total_def_att.append(df['Def Rush Att'].iloc[i] + df['Def Pass Att'].iloc[i])
        
    df['Off Tot Att'] = total_off_att
    df['Def Tot Att'] = total_def_att
    df['Tot Att'] = df['Off Tot Att'] + df['Def Tot Att']
    
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (df['Def Tot Att'][i]/df['Tot Att'][i], df['Off Tot Att'][i]/df['Tot Att'][i]), frameon=False)
        ax.add_artist(ab)

    x_mean = (df['Def Tot Att']/df['Tot Att']).mean()
    y_mean = (df['Off Tot Att']/df['Tot Att']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    # Set labels and title
    ax.set_xlabel('Def %', fontsize=12)
    ax.set_ylabel('Off %', fontsize=12)
    ax.set_title(f'{year} Week {weeks}: Defense Att vs Offense Att Linearized', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Def Tot Att']/df['Tot Att']).min() - 0.025, (df['Off Tot Att']/df['Tot Att']).max() + 0.025)
    plt.ylim((df['Off Tot Att']/df['Tot Att']).min() - 0.025, (df['Off Tot Att']/df['Tot Att']).max() + 0.025)
    save_fig(year, f'Team_RushAtt_PassAtt_Both_Linearized.png')
    plt.show()
    print('Team_RushAtt_PassAtt_Both_Linearized Completed')
    
def Player_All_Passing_Target_Share(db_name, weeks, year):
    df = PullFromDatabase.team_off_target_share_plays(db_name)
    df = df.groupby('Player', as_index=False).agg({
    'shortname': 'first',  # Keep the first occurrence of shortname
    'Off Pass Att': 'first',
    'Rx Tgts': 'sum',
    # Add other columns here with their respective aggregation functions
})
    
    df['Tgt Share'] = (df['Rx Tgts'] / df['Off Pass Att'])*100
    
    df = df[df['Tgt Share'] > df['Tgt Share'].mean()]
    df.reset_index(inplace=True)
    
    tgts_threshold = 10
    
    df = df[(df['Tgt Share'] > tgts_threshold)]
    df.reset_index(inplace=True)
        
    # Create scatter plot with team logos as markers
    fig, ax = plt.subplots(figsize=(12, 9))

    zoom = 0.05

    for index, row in df.iterrows():
        plt.text(row['Off Pass Att'], (row['Tgt Share'])+.5, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
        
    ax.scatter(df['Off Pass Att'], df['Tgt Share'], alpha=0.5, s=0)
    
    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((df['Off Pass Att'])[i], (df['Tgt Share'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (df['Off Pass Att']).mean()
    y_mean = (df['Tgt Share']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    # Set labels and title
    ax.set_xlabel('Total Team Passing Attempts', fontsize=12)
    ax.set_ylabel('Target Share (%)', fontsize=12)
    ax.set_title(f'{year} Week {weeks}: Passing Target Share Percentage by Team', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Off Pass Att']).min() - 10, (df['Off Pass Att']).max() + 10)
    plt.ylim((df['Tgt Share']).min() - 1.25, (df['Tgt Share']).max() + 1.25)
    save_fig(year, f'Player_All_Passing_Target_Share.png')
    plt.show()
    print('Player_All_Passing_Target_Share Completed')


def Player_WR_TPG_vs_YPR(db_name, weeks, year):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    wr_receiving_df_parsed = df[(df['Rx Tgts'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(wr_receiving_df_parsed['Rx Tgts'] / weeks, wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec'], alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rx Tgts'] / weeks, (row['Rx Yds'] / row['Rx Rec'])+0.25, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')

    for i, team in enumerate(wr_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['Rx Tgts'] / weeks)[i], (wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (wr_receiving_df_parsed['Rx Tgts'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: WR Targets per Game vs Yards per Reception', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Yards per Reception', fontsize=12)
    save_fig(year, f'Player_WR_TPG_vs_YPR.png')
    plt.show()
    print('Player_WR_TPG_vs_YPR Completed')


def Player_WR_RPG_vs_YPR(db_name, weeks, year):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    wr_receiving_df_parsed = df[(df['Rx Tgts'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Rx Rec'] / weeks, wr_receiving_df_parsed['Rx Yds'] / weeks, alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rx Rec'] / weeks, (row['Rx Yds'] / weeks)+2, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
        
    for i, team in enumerate(wr_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['Rx Rec'] / weeks)[i], (wr_receiving_df_parsed['Rx Yds'] / weeks)[i]), frameon=False,zorder=1)
        ax.add_artist(ab)


    x_mean = (wr_receiving_df_parsed['Rx Rec'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rx Yds'] / weeks).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))


    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: WR Receptions per Game vs Yards per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Receptions per Game', fontsize=12)
    plt.ylabel('Yards per Game', fontsize=12)
    plt.tight_layout()
    save_fig(year, f'Player_WR_RPG_vs_YPR.png')
    plt.show()
    print('Player_WR_RPG_vs_YPR Completed')
    

def Player_WR_TPG_vs_RPG(db_name, weeks, year):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    wr_receiving_df_parsed = df[(df['Rx Tgts'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Rx Tgts'] / weeks, wr_receiving_df_parsed['Rx Rec'] / wr_receiving_df_parsed['Rx Tgts'], alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rx Tgts'] / weeks, (row['Rx Rec'] / row['Rx Tgts'])+0.01, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')

    for i, team in enumerate(wr_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['Rx Tgts'] / weeks)[i], (wr_receiving_df_parsed['Rx Rec'] / wr_receiving_df_parsed['Rx Tgts'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (wr_receiving_df_parsed['Rx Tgts'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rx Rec'] / wr_receiving_df_parsed['Rx Tgts']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: WR Targets per Game vs Receptions per Target', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Receptions per Target', fontsize=12)
    plt.tight_layout()
    save_fig(year, f'Player_WR_TPG_vs_RPG.png')
    plt.show()
    print('Player_WR_TPG_vs_RPG Completed')

def Player_TE_TPG_vs_RPG(db_name, weeks, year):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    te_receiving_df_parsed = df[(df['Rx Tgts'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'TE')]
    te_receiving_df_parsed.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(te_receiving_df_parsed['Rx Tgts'] / weeks, te_receiving_df_parsed['Rx Rec'] / te_receiving_df_parsed['Rx Tgts'], alpha=0.5, s=0)

    for index, row in te_receiving_df_parsed.iterrows():
        plt.text(row['Rx Tgts'] / weeks, (row['Rx Rec'] / row['Rx Tgts'])+0.005, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
    
    for i, team in enumerate(te_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((te_receiving_df_parsed['Rx Tgts'] / weeks)[i], (te_receiving_df_parsed['Rx Rec'] / te_receiving_df_parsed['Rx Tgts'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (te_receiving_df_parsed['Rx Tgts'] / weeks).mean()
    y_mean = (te_receiving_df_parsed['Rx Rec'] / te_receiving_df_parsed['Rx Tgts']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: TE Targets per Game vs Receptions per Target', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Receptions per Target', fontsize=12)
    plt.tight_layout()
    save_fig(year, f'Player_TE_TPG_vs_RPG.png')
    plt.show()
    print('Player_TE_TPG_vs_RPG Completed')
    
def Player_WR_RPG_vs_TDPR(db_name, weeks, year):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    wr_receiving_df_parsed = df[(df['Rx Tgts'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Rx Rec'] / weeks, wr_receiving_df_parsed['Rx TD'] / wr_receiving_df_parsed['Rx Rec'], alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rx Rec'] / weeks, (row['Rx TD'] / row['Rx Rec'])+0.005, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')


    for i, team in enumerate(wr_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['Rx Rec'] / weeks)[i], (wr_receiving_df_parsed['Rx TD'] / wr_receiving_df_parsed['Rx Rec'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)


    x_mean = (wr_receiving_df_parsed['Rx Rec'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rx TD'] / wr_receiving_df_parsed['Rx Rec']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: WR Receptions per Game vs TDs per Reception', fontsize=16, fontweight='bold')
    plt.xlabel('Receptions per Game', fontsize=12)
    plt.ylabel('TDs per Reception', fontsize=12)
    save_fig(year, f'Player_WR_RPG_vs_TDPR.png')
    plt.show()
    print('Player_WR_RPG_vs_TDPR Completed')


def Player_RB_YPG_vs_TDPG(db_name, weeks, year):
    receiving_df = PullFromDatabase.receiving(db_name)
    receiving_df.drop_duplicates(inplace=True)
    rushing_df = PullFromDatabase.rushing(db_name)
    rushing_df.drop_duplicates(inplace=True)
    

    Att_threshold = 5*weeks
    
    rb_rushing_df_parsed = rushing_df[(rushing_df['Rush Att'] > Att_threshold) & (rushing_df['POS'] == "RB")]

    fig, ax = plt.subplots(figsize=(12,9))

    rb_rushing_df_parsed['Rush Yds'] = rb_rushing_df_parsed['Rush Yds'].astype(float)
    rb_rushing_df_parsed['Rush TD'] = rb_rushing_df_parsed['Rush TD'].astype(float)
    rb_rushing_df_parsed.reset_index(inplace=True)

    ax.scatter(rb_rushing_df_parsed['Rush Yds'].astype(float) / weeks, rb_rushing_df_parsed['Rush TD'].astype(float) / weeks, alpha=0.5, s=0)

    for index, row in rb_rushing_df_parsed.iterrows():
        plt.text(row['Rush Yds'] / weeks, (row['Rush TD'] / weeks)+0.02, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')

    for i, team in enumerate(rb_rushing_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((rb_rushing_df_parsed['Rush Yds']/weeks)[i], (rb_rushing_df_parsed['Rush TD'] / weeks)[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (rb_rushing_df_parsed['Rush Yds'].astype(float) / weeks).mean()
    y_mean = (rb_rushing_df_parsed['Rush TD'].astype(float) / weeks).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    ax.grid(True, which='both', axis='both', linewidth=0.75, linestyle='solid', alpha=0.75, color='#d6d6d6')

    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)

    #ax.tick_params(axis='both', which='both', length=0)

    plt.title(f'{year} Week {weeks}: RB Yards and TDs per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Game', fontsize=12, fontweight='bold')
    plt.ylabel('TDs per Game', fontsize=12, fontweight='bold')
    plt.tight_layout()
    save_fig(year, f'Player_RB_YPG_vs_TDPG.png')
    plt.show()
    print('Player_RB_YPG_vs_TDPG Completed')
    
    
def Player_RB_YPG(db_name, weeks, year):
    receiving_df = PullFromDatabase.receiving(db_name)
    receiving_df.drop_duplicates(inplace=True)
    rushing_df = PullFromDatabase.rushing(db_name)
    rushing_df.drop_duplicates(inplace=True)
    
    Att_threshold = 5*weeks
    Tgts_threshold = 2*weeks
    rush_yards_threshold = 10 #by week already
    yards_threshold = 5 #by week already
    
    rb_receiving_df_parsed = receiving_df[(receiving_df['Rx Tgts'] > Tgts_threshold) & (receiving_df['POS'] == 'RB')]
    rb_rushing_df_parsed = rushing_df[(rushing_df['Rush Att'] > Att_threshold) & (rushing_df['POS'] == "RB")]
    
    rb_rushing_df_parsed['Rush Yds'] = rb_rushing_df_parsed['Rush Yds'].astype(float)
    rb_receiving_df_parsed['Rx Yds'] = rb_receiving_df_parsed['Rx Yds'].astype(float)

    rb_df = pd.merge(rb_rushing_df_parsed, rb_receiving_df_parsed, on='Player')
    rb_parsed = rb_df[((rb_df['Rush Yds'].astype(float) / weeks) > rush_yards_threshold) & ((rb_df['Rx Yds'].astype(float)/weeks) > yards_threshold)]
    rb_parsed.reset_index(inplace=True)
    
    
    fig, ax = plt.subplots(figsize=(12,9))

    #kmeans = KMeans(n_clusters = 8)
    #kmeans.fit(rb_parsed[['Rush Yds', 'Rx Yds']])

    ##labels = kmeans.predict(rb_parsed[['Rush Yds', 'Rx Yds']])

    #plt.scatter(rb_parsed['Rush Yds'].astype(float) / weeks, rb_parsed['Rx Yds'].astype(float) / weeks, c=kmeans.labels_, cmap='gist_rainbow', s=0.0001)
    plt.scatter(rb_parsed['Rush Yds'].astype(float) / weeks, rb_parsed['Rx Yds'].astype(float) / weeks, s=0)


    ##ax.scatter(rb_parsed['Rush Yds'].astype(float) / 17, rb_parsed['Rx Yds'].astype(float) / 17, alpha=0.5)

    for index, row in rb_parsed.iterrows():
        plt.text(row['Rush Yds'] / weeks, (row['Rx Yds'] / weeks)+0.5, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')


    for i, team in enumerate(rb_parsed['shortname_x']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((rb_parsed['Rush Yds']/weeks)[i], (rb_parsed['Rx Yds']/weeks)[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (rb_parsed['Rush Yds'].astype(float) / weeks).mean()
    y_mean = (rb_parsed['Rx Yds'].astype(float) / weeks).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    ax.grid(True, which='both', axis='both', linewidth=0.75, linestyle='solid', alpha=0.75, color='#d6d6d6')

    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)

    #ax.tick_params(axis='both', which='both', length=0)


    plt.title(f'{year} Week {weeks}: RB Rushing and Recieving Yards per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Rushing Yards per Game', fontsize=12, fontweight='bold')
    plt.ylabel('Recieving Yards per Game', fontsize=12, fontweight='bold')
    plt.tight_layout()
    save_fig(year, f'Player_RB_YPG.png')
    #plt.savefig(f'Player_RB_YPG.png', dpi=450, bbox_inches='tight')
    plt.show()
    print('Player_RB_YPG Completed')

def Player_QB_Top12(db_name, weeks, year):
    qb_df = PullFromDatabase.qb(db_name)
    qb_df.replace(np.nan, 0, inplace=True)
    qb_df['fantasy_points'] = (qb_df['Pass Yds'].astype(float)*0.04) + (qb_df['Pass TD'].astype(float)*4) + (qb_df['Rush Yds'].astype(float)*0.1) + (qb_df['Rush TD'].astype(float)*6) - (qb_df['Pass INT'].astype(float)*1) - (qb_df['Fum'].astype(float)*2)
    
    qb_df_parsed3 = qb_df.sort_values(by='fantasy_points', ascending=False)[:32]
    
    qb_df_parsed3['PassYds/G_per_100%'] = ((qb_df_parsed3['Pass Yds'] / weeks) / (qb_df_parsed3['Pass Yds'] / weeks).max()) * 100
    qb_df_parsed3['Cmp%'] = (qb_df_parsed3['Pass Cmp'] / qb_df_parsed3['Pass Att']).astype(float)
    qb_df_parsed3['Cmp%_per_100%'] = ((qb_df_parsed3['Cmp%'] / qb_df_parsed3['Cmp%'].max()) * 100)
    qb_df_parsed3['Yds/Att_per_100%'] = ((qb_df_parsed3['Pass YPA'] / qb_df_parsed3['Pass YPA'].max()) * 100)
    qb_df_parsed3['PassTD/G_per_100%'] = ((qb_df_parsed3['Pass TD'] / weeks) / (qb_df_parsed3['Pass TD'] / weeks).max()) * 100
    qb_df_parsed3['RushYds/G_per_100%'] = ((qb_df_parsed3['Rush Yds'] / weeks) / (qb_df_parsed3['Rush Yds'] / weeks).max()) * 100
    qb_df_parsed3['RushTD/G_per_100%'] = ((qb_df_parsed3['Rush TD'] / weeks) / (qb_df_parsed3['Rush TD'] / weeks).max()) * 100
    qb_df_parsed3['anti_int'] = 1 - (qb_df_parsed3['Pass INT'] / qb_df_parsed3['Pass Att'])
    qb_df_parsed3['anti_int_per_100%'] = (qb_df_parsed3['anti_int'] / qb_df_parsed3['anti_int'].max()) * 100
    qb_df_parsed3['anti_fum'] = 1 - (qb_df_parsed3['Fum'] / qb_df_parsed3['Rush Att'])
    qb_df_parsed3['anti_fum_per_100%'] = (qb_df_parsed3['anti_fum'] / qb_df_parsed3['anti_fum'].max()) * 100
    
    qb_df_parsed3_t12 = qb_df_parsed3.sort_values(by='fantasy_points', ascending=False)[:12]
    qb_df_parsed3_t12[['PassYds/G_per_100%', 'Cmp%_per_100%', 'Yds/Att_per_100%', 'PassTD/G_per_100%', 'anti_int_per_100%','RushTD/G_per_100%', 'anti_fum_per_100%']] = qb_df_parsed3_t12[['PassYds/G_per_100%', 'Cmp%_per_100%', 'Yds/Att_per_100%', 'PassTD/G_per_100%', 'anti_int_per_100%','RushTD/G_per_100%', 'anti_fum_per_100%']].astype(float)
        
    categories = ['PassYds/G_per_100%', 'Cmp%_per_100%', 'Yds/Att_per_100%', 'PassTD/G_per_100%', 'anti_int_per_100%', 'RushTD/G_per_100%', 'anti_fum_per_100%']
    
    fig, axs = plt.subplots(3, 4, figsize=(20, 15), subplot_kw=dict(polar=True))
    fig.subplots_adjust(hspace=0.5)
    axs = axs.flatten() 

    cats = ['PassYds/G', 'Cmp %', 'Yds/PassAtt', 'PassTD/G', 'Anti-Int', 'RushTD/G', 'Anti-Fumble']


    for ax, (index, row) in zip(axs, qb_df_parsed3_t12.iterrows()):
        values = row[categories].tolist()
        values += values[:1] 
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1] 
        
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=row['Player'])
        ax.fill(angles, values, alpha=0.1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(cats)
        ax.set_title(row['Player'], size=12, color='black', y=1.1, fontweight='bold')

    for i in range(len(qb_df_parsed3_t12), len(axs)):
        axs[i].axis('off')

    plt.suptitle(f'{year} Week {weeks}: Top 12 QB Radar Charts', fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_fig(year, f'Player_QB_Top12')
    #plt.savefig(f'Player_QB_Top12', dpi=450, bbox_inches='tight')
    plt.show()
    print('Player_QB_Top12 Completed')

def Player_QB_Top12_1(db_name, weeks, year):
    qb_df = PullFromDatabase.qb(db_name)
    qb_df.replace(np.nan, 0, inplace=True)
    qb_df['fantasy_points'] = (qb_df['Pass Yds'].astype(float)*0.04) + (qb_df['Pass TD'].astype(float)*4) + (qb_df['Rush Yds'].astype(float)*0.1) + (qb_df['Rush TD'].astype(float)*6) - (qb_df['Pass INT'].astype(float)*1) - (qb_df['Fum'].astype(float)*2)
    
    qb_df_parsed = qb_df.sort_values(by='fantasy_points', ascending=False)[:12]
    
    qb_df_parsed['anti_int'] = 1 - (qb_df_parsed['Pass INT'] / qb_df_parsed['Pass Att'])
    qb_df_parsed['anti_fum'] = 1 - (qb_df_parsed['Fum'] / qb_df_parsed['Rush Att'])
    qb_df_parsed['Cmp%'] = (qb_df_parsed['Pass Cmp'] / qb_df_parsed['Pass Att']).astype(float)
    qb_df_parsed['PYds/G'] = (qb_df_parsed['Pass Yds'] / qb_df_parsed['Pass Att']).astype(float)
    qb_df_parsed[['Pass YPA', 'Cmp%', 'anti_int', 'Pass TD', 'Rush TD', 'anti_fum']] = qb_df_parsed[['Pass YPA', 'Cmp%', 'anti_int', 'Pass TD', 'Rush TD', 'anti_fum']].astype(float)

    qb_df_parsed_2 = qb_df_parsed[['Player', 'Pass YPA', 'Cmp%', 'anti_int', 'Pass TD', 'Rush TD', 'anti_fum']]
    
    categories = ['Pass YPA', 'Cmp%', 'anti_int', 'Pass TD', 'Rush TD', 'anti_fum']
    N = len(categories)

    # Normalize data function by dividing by max values
    def normalize(df):
        result = df.copy()
        for feature_name in df.columns:
            max_value = df[feature_name].max()
            result[feature_name] = df[feature_name] / max_value
        return result

    # Radar plot function
    def create_radar_chart(ax, angles, player_data):
        ax.plot(angles, player_data, linewidth=2)
        ax.fill(angles, player_data, alpha=0.25)
        ax.set_yticklabels([])

    # Prepare data
    qb_df_parsed_normalized = normalize(qb_df_parsed[categories])
    data_to_plot = qb_df_parsed_normalized.values

    # Create radar chart for each quarterback
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    player_names = qb_df_parsed['Player'].values

    fig, axs = plt.subplots(3, 4, subplot_kw=dict(polar=True), figsize=(15, 10))
    plt.suptitle(f'{year} Week {weeks}: Top 12 Fantasy QBs', fontsize=16, fontweight='bold')

    for i, ax in enumerate(axs.flatten()):
        if i < len(data_to_plot):
            create_radar_chart(ax, angles, np.concatenate((data_to_plot[i], [data_to_plot[i][0]])))
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_title(player_names[i], size=12, color='black', y=1.1)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_fig(year, f'Player_QB_Top12_1.png')
    #plt.savefig(f'Player_QB_Top12_1.png', dpi=450, bbox_inches='tight')
    plt.show()
    print('Player_QB_Top12_1 Completed')

def Player_K_NetYards_vs_Touchback(db_name, weeks, year):
    df = PullFromDatabase.punters(db_name)
    
    df = df[(df['Punts'] > 2*weeks)]
    df.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(df['Net Avg'], df['TB'], alpha=0.5, s=0)

    for index, row in df.iterrows():
        plt.text(row['Net Avg'], row['TB']+0.1, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
        
    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((df['Net Avg'])[i], (df['TB'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    
    x_mean = (df['Net Avg']).mean()
    y_mean = (df['TB']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: Average Net Yards per Punt vs Touchback Count', fontsize=16, fontweight='bold')
    plt.xlabel('Average Net Yards per Punt', fontsize=12)
    plt.ylabel('Touchback Count', fontsize=12)
    plt.savefig(f'Player_K_NetYards_vs_Touchback.png', dpi=450)
    plt.show()
    print('Player_K_NetYards_vs_Touchback Completed')
    
def Player_QB_YPA_vs_CmpPct(db_name, weeks, year):
    df = PullFromDatabase.passing(db_name)
    
    att_threshold = 10*weeks
    
    df = df[(df['Pass Att'] > att_threshold)]
    df.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))
    
    df['Cmp %'] = (df['Pass Cmp'] / df['Pass Att']).astype(float)

    x_mean = (df['Pass YPA']).mean()
    y_mean = (df['Cmp %']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    
    ax.scatter(df['Pass YPA'], df['Cmp %'], alpha=0.5, s=0)

    for index, row in df.iterrows():
        plt.text(row['Pass YPA'], row['Cmp %']+0.75, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
        
    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((df['Pass YPA'])[i], (df['Cmp %'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)


    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: Yards per Attempt vs Completion Percentage', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Attempt', fontsize=12)
    plt.ylabel('Completion Percentage', fontsize=12)
    plt.tight_layout()
    save_fig(year, f'Player_QB_YPA_vs_CmpPct.png')
    #plt.savefig(f'Player_QB_YPA_vs_CmpPct.png', dpi=450)
    plt.show()
    print('Player_QB_YPA_vs_CmpPct Completed')
    
def Player_QB_YPG_vs_TD(db_name, weeks, year):
    df = PullFromDatabase.passing(db_name)
    
    att_threshold = 10*weeks
    
    df = df[(df['Pass Att'] > att_threshold)]
    df.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    x_mean = (df['Pass Yds'] / weeks).mean()
    y_mean = (df['Pass TD']/ weeks).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    
    ax.scatter(df['Pass Yds']/ weeks, df['Pass TD']/ weeks, alpha=0.5, s=0)

    for index, row in df.iterrows():
        plt.text(row['Pass Yds']/ weeks, (row['Pass TD']/ weeks)+0.05, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')
        
    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((df['Pass Yds']/ weeks)[i], (df['Pass TD']/ weeks)[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title(f'{year} Week {weeks}: Yards vs Touchdowns per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Game', fontsize=12)
    plt.ylabel('Touchdowns per Game', fontsize=12)
    plt.tight_layout()
    save_fig(year, f'Player_QB_YPG_vs_TD.png')
    #plt.savefig(f'Player_QB_YPG_vs_TD.png', dpi=450)
    plt.show()
    print('Player_QB_YPG_vs_TD Completed')SS

def Team_FFScoring_vs_Allowed_Def(db_name, weeks, year):
    df = PullFromDatabase.team_total_def(db_name)
    #(td, points_allowed, sacks, ints, fum_rec, safety, forced_fum, blocked_kick)
    # Sums the passing and rushing defenses, mulitplies by 7 (includes PATs), and divides by weeks 
    df['Points_Allowed'] = ((df['Rush TD'].astype(float) + df['Pass TD'].astype(float)) * 7) / weeks
    df['Points_Scored'] = (df['INT TD'].astype(float) + df['FR TD'].astype(float)) / weeks

    fantasy_points = []
    for i in range(len(df)):
        fantasy_points.append(FantasyCalc.Team_D(df['Points_Scored'][i], df['Points_Allowed'][i], df['Sck'][i], df['Pass INT'][i], df['FR'][i], df['SFTY'][i], df['FF'][i]))
    df['Fantasy_Points'] = fantasy_points

    df.reset_index(inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,9))

    x_mean = (df['Fantasy_Points']/ weeks).mean()
    y_mean = (df['Points_Allowed']/ weeks).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5), zorder=0)
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5), zorder=0)
    
    ax.scatter(df['Fantasy_Points']/ weeks, df['Points_Allowed']/ weeks, alpha=0.5, s=0)

    for i, team in enumerate(df['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.05)
        ab = AnnotationBbox(imagebox, ((df['Fantasy_Points']/ weeks)[i], (df['Points_Allowed']/ weeks)[i]), frameon=False, zorder=2)
        ax.add_artist(ab)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--', zorder=0)

    plt.title(f'{year} Week {weeks}: Team Defense Fantasy Points vs TDs Allowed per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Fantasy Points per Game', fontsize=12)
    plt.ylabel('TDs Allowed per Game', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'team_defensive_fantasy_scoring_vs_allowed.png', dpi=450)
    plt.show()
    print('Team_FFScoring_vs_Allowed_Def Completed')


if __name__ == '__main__':
    nfl_state = SleeperInfo.get_nfl_state()
    if nfl_state['season_type'] != 'post':
        year = nfl_state['season']
        weeks = nfl_state['week']
    else:
        year = 2024
        weeks = 18

    db_name = rf'database\{year}.db'

    current_directory = os.getcwd()
    # Ensure the plots directory exists
    plots_dir = os.path.join(current_directory, f'{year}/plots')
    os.makedirs(plots_dir, exist_ok=True)
    # Change the current working directory to the plots directory
    os.chdir(plots_dir)
    
    Team_RushAtt_PassAtt_Off(db_name, weeks, year)
    Team_RushAtt_PassAtt_Off_Linearized(db_name, weeks, year)
    Team_RushAtt_PassAtt_Both(db_name, weeks, year)
    Team_RushAtt_PassAtt_Both_Linearized(db_name, weeks, year)
    Player_All_Passing_Target_Share(db_name, weeks, year)
    Player_WR_TPG_vs_YPR(db_name, weeks, year)
    Player_WR_RPG_vs_YPR(db_name, weeks, year)
    Player_WR_TPG_vs_RPG(db_name, weeks, year)
    Player_WR_RPG_vs_TDPR(db_name, weeks, year)
    Player_RB_YPG_vs_TDPG(db_name, weeks, year)
    Player_RB_YPG(db_name, weeks, year)
    Player_QB_Top12_1(db_name, weeks, year)
    Player_TE_TPG_vs_RPG(db_name, weeks, year)
    Player_QB_YPG_vs_TD(db_name, weeks, year)
    Player_QB_YPA_vs_CmpPct(db_name, weeks, year)
    #Player_K_NetYards_vs_Touchback(db_name, weeks, year)
    #Team_FFScoring_vs_Allowed_Def(db_name, weeks, year)
    
    
