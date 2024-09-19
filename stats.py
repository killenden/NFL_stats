
import utils
import pandas as pd
import os
import PullFromDatabase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans

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
    ax.set_xlabel('Rush Att', fontsize=12)
    ax.set_ylabel('Pass Att', fontsize=12)
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim(df['Rush_Att'].min() - 1, df['Rush_Att'].max() + 1)
    plt.ylim(df['Pass_Att'].min() - 1, df['Pass_Att'].max() + 1)
    plt.savefig('2024/plots/Team_Attempts.png', dpi=450)
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
    ax.set_xlabel('Rush Att', fontsize=12)
    ax.set_ylabel('Pass Att', fontsize=12)
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Rush_Att']/df['Tot_Att']).min() - 0.025, (df['Rush_Att']/df['Tot_Att']).max() + 0.025)
    plt.ylim((df['Pass_Att']/df['Tot_Att']).min() - 0.025, (df['Pass_Att']/df['Tot_Att']).max() + 0.025)
    plt.savefig('2024/plots/Team_Attempts_Pct.png', dpi=450)
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
    ax.set_xlabel('Tot_Def_Att', fontsize=12)
    ax.set_ylabel('Tot_Off_Att', fontsize=12)
    ax.set_title('Scatter Plot of Defense Att vs Offense Att with Team Logos', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Tot_Def_Att']).min() - 0.025, (df['Tot_Off_Att']).max() + 0.025)
    plt.ylim((df['Tot_Off_Att']).min() - 0.025, (df['Tot_Off_Att']).max() + 0.025)
    plt.savefig('2024/plots/Team_Attempts_Both.png', dpi=450)
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
    ax.set_xlabel('Def %', fontsize=12)
    ax.set_ylabel('Off %', fontsize=12)
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Tot_Def_Att']/df['Tot_Att']).min() - 0.025, (df['Tot_Off_Att']/df['Tot_Att']).max() + 0.025)
    plt.ylim((df['Tot_Off_Att']/df['Tot_Att']).min() - 0.025, (df['Tot_Off_Att']/df['Tot_Att']).max() + 0.025)
    plt.savefig('2024/plots/Team_Attempts_Both_Pct.png', dpi=450)
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
    ax.set_xlabel('Total Team Passing Attempts', fontsize=12)
    ax.set_ylabel('Target Share', fontsize=12)
    ax.set_title('Scatter Plot of Rush Att vs Pass Att with Team Logos', fontsize=16, fontweight='bold')
    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    # Adjust plot limits
    plt.xlim((df['Pass_Off_Att']).min() - 10, (df['Pass_Off_Att']).max() + 10)
    plt.ylim((df['Tgt_Share']).min() - 0.0125, (df['Tgt_Share']).max() + 0.0125)
    plt.savefig('2024/plots/Target_Share.png', dpi=450)
    plt.show()


def TPG_vs_YPR(db_name, weeks):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    wr_receiving_df_parsed = df[(df['Tgts'] > threshold) & (df['Rec'] > 0) & (df['POS'] == 'WR')]
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(wr_receiving_df_parsed['Tgts'] / weeks, wr_receiving_df_parsed['Yds'] / wr_receiving_df_parsed['Rec'], alpha=0.5)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Tgts'] / weeks, row['Yds'] / row['Rec'], row['Player'], fontsize=9, ha='right')

    x_mean = (wr_receiving_df_parsed['Tgts'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Yds'] / wr_receiving_df_parsed['Rec']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: WR Targets per Game vs Yards per Reception', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Yards per Reception', fontsize=12)
    plt.savefig('2024/plots/TPG_vs_YPR.png', dpi=450)
    plt.show()


def RPG_YPG(db_name, weeks):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    wr_receiving_df_parsed = df[(df['Tgts'] > threshold) & (df['Rec'] > 0) & (df['POS'] == 'WR')]
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Rec'] / weeks, wr_receiving_df_parsed['Yds'] / weeks, alpha=0.5)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rec'] / weeks, row['Yds'] / weeks, row['Player'], fontsize=9, ha='right')

    x_mean = (wr_receiving_df_parsed['Rec'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Yds'] / weeks).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)


    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: WR Receptions per Game vs Yards per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Receptions per Game', fontsize=12)
    plt.ylabel('Yards per Game', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/RPG_YPG.png', dpi=450)
    plt.show()
    
    

def TPG_RPG(db_name, weeks):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    wr_receiving_df_parsed = df[(df['Tgts'] > threshold) & (df['Rec'] > 0) & (df['POS'] == 'WR')]
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Tgts'] / weeks, wr_receiving_df_parsed['Rec'] / wr_receiving_df_parsed['Tgts'], alpha=0.5)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Tgts'] / weeks, row['Rec'] / row['Tgts'], row['Player'], fontsize=9, ha='right')

    x_mean = (wr_receiving_df_parsed['Tgts'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rec'] / wr_receiving_df_parsed['Tgts']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: WR Targets per Game vs Receptions per Target', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Receptions per Target', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/TPG_RPG.png', dpi=450)
    plt.show()

def TE_TPG_RPG(db_name, weeks):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    wr_receiving_df_parsed = df[(df['Tgts'] > threshold) & (df['Rec'] > 0) & (df['POS'] == 'TE')]
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Tgts'] / weeks, wr_receiving_df_parsed['Rec'] / wr_receiving_df_parsed['Tgts'], alpha=0.5)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Tgts'] / weeks, row['Rec'] / row['Tgts'], row['Player'], fontsize=9, ha='right')

    x_mean = (wr_receiving_df_parsed['Tgts'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rec'] / wr_receiving_df_parsed['Tgts']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: TE Targets per Game vs Receptions per Target', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Receptions per Target', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/TE_TPG_RPG.png', dpi=450)
    plt.show()
    
    
def RPG_vs_TDPR(db_name, weeks):
    df = PullFromDatabase.receiving(db_name)
    df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    wr_receiving_df_parsed = df[(df['Tgts'] > threshold) & (df['Rec'] > 0) & (df['POS'] == 'WR')]
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(wr_receiving_df_parsed['Rec'] / weeks, wr_receiving_df_parsed['TD'] / wr_receiving_df_parsed['Rec'], alpha=0.5)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['Rec'] / weeks, row['TD'] / row['Rec'], row['Player'], fontsize=9, ha='right')

    x_mean = (wr_receiving_df_parsed['Rec'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['TD'] / wr_receiving_df_parsed['Rec']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: WR Receptions per Game vs TDs per Reception', fontsize=16, fontweight='bold')
    plt.xlabel('Receptions per Game', fontsize=12)
    plt.ylabel('TDs per Reception', fontsize=12)
    plt.savefig('2024/plots/RPG_vs_TDPR.png', dpi=450)
    plt.show()


def RB_YPG_vs_TDPG(db_name, weeks):
    receiving_df = PullFromDatabase.receiving(db_name)
    receiving_df.drop_duplicates(inplace=True)
    rushing_df = PullFromDatabase.rushing(db_name)
    rushing_df.drop_duplicates(inplace=True)
    
    threshold = 1
    
    rb_receiving_df_parsed = receiving_df[(receiving_df['Tgts'] > threshold) & (receiving_df['POS'] == 'RB')]
    rb_rushing_df_parsed = rushing_df[(rushing_df['Att'] > threshold) & (rushing_df['POS'] == "RB")]

    fig, ax = plt.subplots(figsize=(12,9))

    rb_rushing_df_parsed['Rush Yds'] = rb_rushing_df_parsed['Rush Yds'].astype(float)
    rb_rushing_df_parsed['TD'] = rb_rushing_df_parsed['TD'].astype(float)

    ax.scatter(rb_rushing_df_parsed['Rush Yds'].astype(float) / weeks, rb_rushing_df_parsed['TD'].astype(float) / weeks, alpha=0.5)

    for index, row in rb_rushing_df_parsed.iterrows():
        plt.text(row['Rush Yds'] / weeks, row['TD'] / weeks, row['Player'], fontsize=9, ha='right')

    x_mean = (rb_rushing_df_parsed['Rush Yds'].astype(float) / weeks).mean()
    y_mean = (rb_rushing_df_parsed['TD'].astype(float) / weeks).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: RB Yards and TDs per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Game', fontsize=12)
    plt.ylabel('TDs per Game', fontsize=12)
    plt.savefig('2024/plots/RB_YPG_vs_TDPG.png', dpi=450)
    plt.show()
    
    
def RB_YPG(db_name, weeks):
    receiving_df = PullFromDatabase.receiving(db_name)
    receiving_df.drop_duplicates(inplace=True)
    rushing_df = PullFromDatabase.rushing(db_name)
    rushing_df.drop_duplicates(inplace=True)
    
    threshold = 1
    rush_yards_threshold = 5
    yards_threshold = 5
    
    rb_receiving_df_parsed = receiving_df[(receiving_df['Tgts'] > threshold) & (receiving_df['POS'] == 'RB')]
    rb_rushing_df_parsed = rushing_df[(rushing_df['Att'] > threshold) & (rushing_df['POS'] == "RB")]
    
    rb_rushing_df_parsed['Rush Yds'] = rb_rushing_df_parsed['Rush Yds'].astype(float)
    rb_receiving_df_parsed['Yds'] = rb_receiving_df_parsed['Yds'].astype(float)

    rb_df = pd.merge(rb_rushing_df_parsed, rb_receiving_df_parsed, on='Player')
    rb_parsed = rb_df[((rb_df['Rush Yds'].astype(float) / weeks) > rush_yards_threshold) & ((rb_df['Yds'].astype(float)/weeks) > yards_threshold)]
    rb_parsed.reset_index(inplace=True)
    
    
    fig, ax = plt.subplots(figsize=(12,9))

    kmeans = KMeans(n_clusters = 8)
    kmeans.fit(rb_parsed[['Rush Yds', 'Yds']])

    ##labels = kmeans.predict(rb_parsed[['Rush Yds', 'Yds']])

    plt.scatter(rb_parsed['Rush Yds'].astype(float) / weeks, rb_parsed['Yds'].astype(float) / weeks, c=kmeans.labels_, cmap='gist_rainbow', s=0.0001)

    ##ax.scatter(rb_parsed['Rush Yds'].astype(float) / 17, rb_parsed['Yds'].astype(float) / 17, alpha=0.5)

    for index, row in rb_parsed.iterrows():
        plt.text(row['Rush Yds'] / weeks, (row['Yds'] / weeks)+1.5, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')

    zoom = 0.02

    for i, team in enumerate(rb_parsed['shortname_x']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, ((rb_parsed['Rush Yds']/weeks)[i], (rb_parsed['Yds']/weeks)[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (rb_parsed['Rush Yds'].astype(float) / weeks).mean()
    y_mean = (rb_parsed['Yds'].astype(float) / weeks).mean()
    ax.axvline(x=x_mean, color='black', linestyle=':', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle=':', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: RB Rushing and Recieving Yards per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Rushing Yards per Game', fontsize=12)
    plt.ylabel('Recieving Yards per Game', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/RB_YPG.png', dpi=450, bbox_inches='tight')
    plt.show()

def Top12QB(db_name, weeks):
    qb_df = PullFromDatabase.qb(db_name)
    qb_df.replace(np.nan, 0, inplace=True)
    qb_df['fantasy_points'] = (qb_df['Pass Yds'].astype(float)*0.04) + (qb_df['Pass_TD'].astype(float)*4) + (qb_df['Rush Yds'].astype(float)*0.1) + (qb_df['Rush_TD'].astype(float)*6) - (qb_df['INT'].astype(float)*1) - (qb_df['Rush FUM'].astype(float)*2)
    
    qb_df_parsed3 = qb_df.sort_values(by='fantasy_points', ascending=False)[:32]
    
    qb_df_parsed3['PassYds/G_per_100%'] = ((qb_df_parsed3['Pass Yds'] / weeks) / (qb_df_parsed3['Pass Yds'] / weeks).max()) * 100
    qb_df_parsed3['Cmp%'] = (qb_df_parsed3['Cmp'] / qb_df_parsed3['Att']).astype(float)
    qb_df_parsed3['Cmp%_per_100%'] = ((qb_df_parsed3['Cmp%'] / qb_df_parsed3['Cmp%'].max()) * 100)
    qb_df_parsed3['Yds/Att_per_100%'] = ((qb_df_parsed3['Yds/Att'] / qb_df_parsed3['Yds/Att'].max()) * 100)
    qb_df_parsed3['PassTD/G_per_100%'] = ((qb_df_parsed3['Pass_TD'] / weeks) / (qb_df_parsed3['Pass_TD'] / weeks).max()) * 100
    qb_df_parsed3['RushYds/G_per_100%'] = ((qb_df_parsed3['Rush Yds'] / weeks) / (qb_df_parsed3['Rush Yds'] / weeks).max()) * 100
    qb_df_parsed3['RushTD/G_per_100%'] = ((qb_df_parsed3['Rush_TD'] / weeks) / (qb_df_parsed3['Rush_TD'] / weeks).max()) * 100
    qb_df_parsed3['anti_int'] = 1 - (qb_df_parsed3['INT'] / qb_df_parsed3['Att'])
    qb_df_parsed3['anti_int_per_100%'] = (qb_df_parsed3['anti_int'] / qb_df_parsed3['anti_int'].max()) * 100
    qb_df_parsed3['anti_fum'] = 1 - (qb_df_parsed3['Rush FUM'] / qb_df_parsed3['Rush_Att'])
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

    plt.suptitle('Top 12 QB Fantasy Performance Radar Charts', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('2024/plots/Top12QB', dpi=450, bbox_inches='tight')
    plt.show()

def Top12QB_1(db_name):
    qb_df = PullFromDatabase.qb(db_name)
    qb_df.replace(np.nan, 0, inplace=True)
    qb_df['fantasy_points'] = (qb_df['Pass Yds'].astype(float)*0.04) + (qb_df['Pass_TD'].astype(float)*4) + (qb_df['Rush Yds'].astype(float)*0.1) + (qb_df['Rush_TD'].astype(float)*6) - (qb_df['INT'].astype(float)*1) - (qb_df['Rush FUM'].astype(float)*2)
    
    qb_df_parsed = qb_df.sort_values(by='fantasy_points', ascending=False)[:12]
    
    qb_df_parsed['anti_int'] = 1 - (qb_df_parsed['INT'] / qb_df_parsed['Att'])
    qb_df_parsed['anti_fum'] = 1 - (qb_df_parsed['Rush FUM'] / qb_df_parsed['Rush_Att'])
    qb_df_parsed['Cmp%'] = (qb_df_parsed['Cmp'] / qb_df_parsed['Att']).astype(float)
    qb_df_parsed['PYds/G'] = (qb_df_parsed['Pass Yds'] / qb_df_parsed['Att']).astype(float)
    qb_df_parsed[['Yds/Att', 'Cmp%', 'anti_int', 'Pass_TD', 'Rush_TD', 'anti_fum']] = qb_df_parsed[['Yds/Att', 'Cmp%', 'anti_int', 'Pass_TD', 'Rush_TD', 'anti_fum']].astype(float)

    qb_df_parsed_2 = qb_df_parsed[['Player', 'Yds/Att', 'Cmp%', 'anti_int', 'Pass_TD', 'Rush_TD', 'anti_fum']]
    
    categories = ['Yds/Att', 'Cmp%', 'anti_int', 'Pass_TD', 'Rush_TD', 'anti_fum']
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
    plt.suptitle('NFL 2024 Week 1: Top 12 Fantasy QBs', fontsize=16, fontweight='bold')

    for i, ax in enumerate(axs.flatten()):
        if i < len(data_to_plot):
            create_radar_chart(ax, angles, np.concatenate((data_to_plot[i], [data_to_plot[i][0]])))
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_title(player_names[i], size=12, color='black', y=1.1)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('2024/plots/Top12QB_1.png', dpi=450, bbox_inches='tight')
    plt.show()

def punting(db_name):
    df = PullFromDatabase.punters(db_name)
    
    df = df[(df['Punts'] > 1)]
    
    fig, ax = plt.subplots(figsize=(12,9))

    ax.scatter(df['Net Avg'], df['TB'], alpha=0.5)

    for index, row in df.iterrows():
        plt.text(row['Net Avg'], row['TB'], row['Player'], fontsize=9, ha='right')
    
    x_mean = (df['Net Avg']).mean()
    y_mean = (df['TB']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: Average Net Yards per Punt vs Touchback Count', fontsize=16, fontweight='bold')
    plt.xlabel('Average Net Yards per Punt', fontsize=12)
    plt.ylabel('Touchback Count', fontsize=12)
    plt.savefig('2024/plots/NYPP_vs_TB.png', dpi=450)
    plt.show()
    
def Passing_YPA_vs_CP(db_name):
    df = PullFromDatabase.passing(db_name)
    
    df = df[(df['Att'] > 20)]
    
    fig, ax = plt.subplots(figsize=(12,9))

    x_mean = (df['Yds/Att']).mean()
    y_mean = (df['Cmp %']).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)
    
    ax.scatter(df['Yds/Att'], df['Cmp %'], alpha=0.5)

    for index, row in df.iterrows():
        plt.text(row['Yds/Att'], row['Cmp %'], row['Player'], fontsize=9, ha='right')

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: Yards per Attempt vs Completion Percentage', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Attempt', fontsize=12)
    plt.ylabel('Completion Percentage', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/Passing_YPA_vs_CP.png', dpi=450)
    plt.show()
    
def Passing_YPG_vs_TD(db_name, weeks):
    df = PullFromDatabase.passing(db_name)
    
    df = df[(df['Att'] > 20)]
    
    fig, ax = plt.subplots(figsize=(12,9))

    x_mean = (df['Pass Yds'] / weeks).mean()
    y_mean = (df['TD']/ weeks).mean()
    ax.axvline(x=x_mean, color='black', linestyle='solid', linewidth=1)
    ax.axhline(y=y_mean, color='black', linestyle='solid', linewidth=1)
    
    ax.scatter(df['Pass Yds']/ weeks, df['TD']/ weeks, alpha=0.5)

    for index, row in df.iterrows():
        plt.text(row['Pass Yds']/ weeks, row['TD']/ weeks, row['Player'], fontsize=9, ha='right')

    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    plt.title('NFL 2024: Yards vs Touchdowns per Game', fontsize=16, fontweight='bold')
    plt.xlabel('Yards per Game', fontsize=12)
    plt.ylabel('Touchdowns per Game', fontsize=12)
    plt.tight_layout()
    plt.savefig('2024/plots/Passing_YPG_vs_TD.png', dpi=450)
    plt.show()





if __name__ == '__main__':
    year = 2024
    weeks = 2
    db_name = rf'database\{year}_database.db'
    #TE_TPG_RPG(db_name, weeks)
    #Passing_YPG_vs_TD(db_name, weeks)
    #Passing_YPA_vs_CP(db_name)
    #punting(db_name)
    #Top12QB_1(db_name)
    #Top12QB(db_name, weeks)
    RB_YPG(db_name, weeks)
    #RB_YPG_vs_TDPG(db_name, weeks)
    #RPG_vs_TDPR(db_name, weeks)
    #TPG_RPG(db_name, weeks)
    #RPG_YPG(db_name, weeks)
    #TPG_vs_YPR(db_name, weeks)
    #Target_Share(db_name)
    #Team_Attempts_Pct(db_name)
    #Team_Attempts_Both(db_name)
    
    
