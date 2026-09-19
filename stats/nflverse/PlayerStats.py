import nflreadpy as nfl
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors as mcolors
#from sklearn.cluster import KMeans
from datetime import date
#https://github.com/nflverse/nflreadpy





def get_team_logo(team_abbr):
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    #file_path = os.path.join(base_dir, 'stats', 'logos', f'{team_abbr}.png')
    file_path = os.path.join(base_dir, 'logos', f'{team_abbr}.png')
    return file_path

def save_fig(year, plot_name):
    #current_directory = os.getcwd()
    # Ensure the plots directory exists
    #plots_dir = os.path.join(current_directory, f'{year}/plots')
    #os.makedirs(plots_dir, exist_ok=True)
    # Change the current working directory to the plots directory
    #os.chdir(plots_dir)
    plt.savefig(f'{plot_name}', dpi=450)
    #change back
    #os.chdir(current_directory)


def team_off_passing(df):
    df = df[['season',
            'week',
            'team',
            'season_type',
            'game_id',
            'opponent_team',
            'completions',
            'attempts',
            'passing_yards',
            'passing_tds',
            'passing_interceptions',
            'sacks_suffered',
            'sack_yards_lost',
            'sack_fumbles',
            'sack_fumbles_lost',
            'passing_air_yards',
            'passing_yards_after_catch',
            'passing_first_downs',
            'passing_epa',
            'passing_cpoe',
            'passing_2pt_conversions',
            'passing_10',
            'passing_16',
            'passing_20',
            'passing_40']]
    return df

def team_stats_season(df):
    df = df.groupby(['team']).agg({
        'completions': 'sum',
        'attempts': 'sum',
        'passing_yards': 'sum',
        'passing_tds': 'sum',
        'passing_interceptions': 'sum',
        'sacks_suffered': 'sum',
        'sack_yards_lost': 'sum',
        'sack_fumbles': 'sum',
        'sack_fumbles_lost': 'sum',
        'passing_air_yards': 'sum',
        'passing_yards_after_catch': 'sum',
        'passing_first_downs': 'sum',
        'passing_epa': 'sum',
        'passing_cpoe': 'sum',
        'passing_2pt_conversions': 'sum',
        'passing_10': 'sum',
        'passing_16': 'sum',
        'passing_20': 'sum',
        'passing_40': 'sum',
        'carries': 'sum',
        'rushing_yards': 'sum',
        'rushing_tds': 'sum',
        'rushing_fumbles': 'sum',
        'rushing_fumbles_lost': 'sum',
        'rushing_first_downs': 'sum',
        'rushing_epa': 'sum',
        'rushing_2pt_conversions': 'sum',
        'rushing_10': 'sum',
        'rushing_12': 'sum',
        'rushing_20': 'sum',
        'rushing_40': 'sum',
        'receptions': 'sum',
        'targets': 'sum',
        'receiving_yards': 'sum',
        'receiving_tds': 'sum',
        'receiving_fumbles': 'sum',
        'receiving_fumbles_lost': 'sum',
        'receiving_air_yards': 'sum',
        'receiving_yards_after_catch': 'sum',
        'receiving_first_downs': 'sum',
        'receiving_epa': 'sum',
        'receiving_2pt_conversions': 'sum',
        'receiving_10': 'sum',
        'receiving_16': 'sum',
        'receiving_20': 'sum',
        'receiving_40': 'sum',
        'special_teams_tds': 'sum',
        'def_tackles_solo': 'sum',
        'def_tackles_with_assist': 'sum',
        'def_tackle_assists': 'sum',
        'def_tackles_for_loss': 'sum',
        'def_tackles_for_loss_yards': 'sum',
        'def_fumbles_forced': 'sum',
        'def_sacks': 'sum',
        'def_sack_yards': 'sum',
        'def_qb_hits': 'sum',
        'def_interceptions': 'sum',
        'def_interception_yards': 'sum',
        'def_pass_defended': 'sum',
        'def_tds': 'sum',
        'def_fumbles': 'sum',
        'def_safeties': 'sum',
        'def_punt_blocks': 'sum',
        'def_pat_blocks': 'sum',
        'def_fg_blocks': 'sum',
        'def_2pt_atts': 'sum',
        'def_2pt_made': 'sum',
        'misc_yards': 'sum',
        'fumble_recovery_own': 'sum',
        'fumble_recovery_yards_own': 'sum',
        'fumble_recovery_opp': 'sum',
        'fumble_recovery_yards_opp': 'sum',
        'fumble_recovery_tds': 'sum',
        'penalties': 'sum',
        'penalty_yards': 'sum',
        'timeouts': 'sum',
        'fumbles_forced_by_opp': 'sum',
        'fumbles_not_forced': 'sum',
        'fumbles_out_of_bounds': 'sum',
        'fumbles_total': 'sum',
        'fumbles_lost_total': 'sum',
        'punt_returns': 'sum',
        'punt_return_yards': 'sum',
        'kickoff_returns': 'sum',
        'kickoff_return_yards': 'sum',
        'fg_made': 'sum',
        'fg_att': 'sum',
        'fg_missed': 'sum',
        'fg_blocked': 'sum',
        'fg_long': 'sum',
        'fg_pct': 'mean',
        'fg_made_0_19': 'sum',
        'fg_made_20_29': 'sum',
        'fg_made_30_39': 'sum',
        'fg_made_40_49': 'sum',
        'fg_made_50_59': 'sum',
        'fg_made_60_': 'sum',
        'fg_missed_0_19': 'sum',
        'fg_missed_20_29': 'sum',
        'fg_missed_30_39': 'sum',
        'fg_missed_40_49': 'sum',
        'fg_missed_50_59': 'sum',
        'fg_missed_60_': 'sum',
        'fg_made_list': 'sum',
        'fg_missed_list': 'sum',
        'fg_blocked_list': 'sum',
        'fg_made_distance': 'sum',
        'fg_missed_distance': 'sum',
        'fg_blocked_distance': 'sum',
        'pat_made': 'sum',
        'pat_att': 'sum',
        'pat_missed': 'sum',
        'pat_blocked': 'sum',
        'pat_pct': 'mean',
        'gwfg_made': 'sum',
        'gwfg_att': 'sum',
        'gwfg_missed': 'sum',
        'gwfg_blocked': 'sum',
        'gwfg_distance': 'sum',
        'pt_att': 'sum',
        'pt_blocked': 'sum',
        'pt_long': 'sum',
        'pt_yards': 'sum',
        'pt_inside_20': 'sum',
        'pt_out_of_bounds': 'sum',
        'pt_downed': 'sum',
        'pt_touchback': 'sum',
        'pt_fair_caught': 'sum',
        'pt_returned': 'sum',
        'pt_return_yards': 'sum',
        'pt_return_tds': 'sum',
        'pt_net_yards': 'sum'
        })
    return df

def player_stats_season(df):
    df = df.groupby(['player_id']).agg({
        'player_name': 'first',
        'player_display_name': 'first',
        'position': 'first',
        'position_group': 'first',
        'headshot_url': 'first',
        'team': 'first',
        'completions': 'sum',
        'attempts': 'sum',
        'passing_yards': 'sum',
        'passing_tds': 'sum',
        'passing_interceptions': 'sum',
        'sacks_suffered': 'sum',
        'sack_yards_lost': 'sum',
        'sack_fumbles': 'sum',
        'sack_fumbles_lost': 'sum',
        'passing_air_yards': 'sum',
        'passing_yards_after_catch': 'sum',
        'passing_first_downs': 'sum',
        'passing_epa': 'sum',
        'passing_cpoe': 'mean',
        'passing_2pt_conversions': 'sum',
        'pacr': 'sum',
        'passing_10': 'sum',
        'passing_16': 'sum',
        'passing_20': 'sum',
        'passing_40': 'sum',
        'carries': 'sum',
        'rushing_yards': 'sum',
        'rushing_tds': 'sum',
        'rushing_fumbles': 'sum',
        'rushing_fumbles_lost': 'sum',
        'rushing_first_downs': 'sum',
        'rushing_epa': 'sum',
        'rushing_2pt_conversions': 'sum',
        'rushing_10': 'sum',
        'rushing_12': 'sum',
        'rushing_20': 'sum',
        'rushing_40': 'sum',
        'receptions': 'sum',
        'targets': 'sum',
        'receiving_yards': 'sum',
        'receiving_tds': 'sum',
        'receiving_fumbles': 'sum',
        'receiving_fumbles_lost': 'sum',
        'receiving_air_yards': 'sum',
        'receiving_yards_after_catch': 'sum',
        'receiving_first_downs': 'sum',
        'receiving_epa': 'sum',
        'receiving_2pt_conversions': 'sum',
        'receiving_10': 'sum',
        'receiving_16': 'sum',
        'receiving_20': 'sum',
        'receiving_40': 'sum',
        'racr': 'sum',
        'target_share': 'mean',
        'air_yards_share': 'mean',
        'wopr': 'mean',
        'special_teams_tds': 'sum',
        'def_tackles_solo': 'sum',
        'def_tackles_with_assist': 'sum',
        'def_tackle_assists': 'sum',
        'def_tackles_for_loss': 'sum',
        'def_tackles_for_loss_yards': 'sum',
        'def_fumbles_forced': 'sum',
        'def_sacks': 'sum',
        'def_sack_yards': 'sum',
        'def_qb_hits': 'sum',
        'def_interceptions': 'sum',
        'def_interception_yards': 'sum',
        'def_pass_defended': 'sum',
        'def_tds': 'sum',
        'def_fumbles': 'sum',
        'def_safeties': 'sum',
        'def_punt_blocks': 'sum',
        'def_pat_blocks': 'sum',
        'def_fg_blocks': 'sum',
        'def_2pt_atts': 'sum',
        'def_2pt_made': 'sum',
        'misc_yards': 'sum',
        'fumble_recovery_own': 'sum',
        'fumble_recovery_yards_own': 'sum',
        'fumble_recovery_opp': 'sum',
        'fumble_recovery_yards_opp': 'sum',
        'fumble_recovery_tds': 'sum',
        'penalties': 'sum',
        'penalty_yards': 'sum',
        'fumbles_forced_by_opp': 'sum',
        'fumbles_not_forced': 'sum',
        'fumbles_out_of_bounds': 'sum',
        'fumbles_total': 'sum',
        'fumbles_lost_total': 'sum',
        'punt_returns': 'sum',
        'punt_return_yards': 'sum',
        'kickoff_returns': 'sum',
        'kickoff_return_yards': 'sum',
        'fg_made': 'sum',
        'fg_att': 'sum',
        'fg_missed': 'sum',
        'fg_blocked': 'sum',
        'fg_long': 'sum',
        'fg_pct': 'mean',
        'fg_made_0_19': 'sum',
        'fg_made_20_29': 'sum',
        'fg_made_30_39': 'sum',
        'fg_made_40_49': 'sum',
        'fg_made_50_59': 'sum',
        'fg_made_60_': 'sum',
        'fg_missed_0_19': 'sum',
        'fg_missed_20_29': 'sum',
        'fg_missed_30_39': 'sum',
        'fg_missed_40_49': 'sum',
        'fg_missed_50_59': 'sum',
        'fg_missed_60_': 'sum',
        'fg_made_list': 'sum',
        'fg_missed_list': 'sum',
        'fg_blocked_list': 'sum',
        'fg_made_distance': 'sum',
        'fg_missed_distance': 'sum',
        'fg_blocked_distance': 'sum',
        'pat_made': 'sum',
        'pat_att': 'sum',
        'pat_missed': 'sum',
        'pat_blocked': 'sum',
        'pat_pct': 'mean',
        'gwfg_made': 'sum',
        'gwfg_att': 'sum',
        'gwfg_missed': 'sum',
        'gwfg_blocked': 'sum',
        'gwfg_distance': 'sum',
        'pt_att': 'sum',
        'pt_blocked': 'sum',
        'pt_long': 'sum',
        'pt_yards': 'sum',
        'pt_inside_20': 'sum',
        'pt_out_of_bounds': 'sum',
        'pt_downed': 'sum',
        'pt_touchback': 'sum',
        'pt_fair_caught': 'sum',
        'pt_returned': 'sum',
        'pt_return_yards': 'sum',
        'pt_return_tds': 'sum',
        'pt_net_yards': 'sum',
        'fantasy_points': 'sum',
        'fantasy_points_ppr': 'sum'
        })
    return df
    
def Team_AirYards(df, weeks, year):
    df = team_off_passing_season(df)
    
    tgts_threshold = 3*weeks
    rec_threshold = 2*weeks
    
    wr_receiving_df_parsed = df[(df['targets'] > tgts_threshold) & (df['Rx Rec'] > rec_threshold) & (df['POS'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(wr_receiving_df_parsed['targets'] / weeks, wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec'], alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['targets'] / weeks, (row['Rx Yds'] / row['Rx Rec'])+0.25, row['Player'], fontsize=9, ha='center',zorder=2,weight='bold')

    for i, team in enumerate(wr_receiving_df_parsed['shortname']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['targets'] / weeks)[i], (wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (wr_receiving_df_parsed['targets'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['Rx Yds'] / wr_receiving_df_parsed['Rx Rec']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    plt.title(f'{formatted_date}: WR Targets per Game vs Yards per Reception', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('Yards per Reception', fontsize=12)
    save_fig(year, f'Player_WR_TPG_vs_YPR.png')
    plt.show()
    print('Player_WR_TPG_vs_YPR Completed')


def Player_RB_CPG_vs_EPAPC(df, weeks, year):   
    # Calibrateable thresholds for filtering WRs based on targets and receptions 
    crs_threshold = 1*weeks
    #rec_threshold = 1*weeks
    
    rb_rushing_df_parsed = df[(df['carries'] > crs_threshold) & (df['position'] == 'RB')]
    rb_rushing_df_parsed.reset_index(inplace=True)
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(rb_rushing_df_parsed['carries'] / weeks, rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries'], alpha=0.5, s=0)
    
    mean_rushing_epa = (rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries']).mean()
    max_rushing_epa = (rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries']).max()
    min_rushing_epa = (rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries']).min()

    for index, row in rb_rushing_df_parsed.iterrows():
        plt.text(row['carries'] / weeks, (row['rushing_epa'] / row['carries']) + (max_rushing_epa - min_rushing_epa) * 0.01, row['player_name'], fontsize=9, ha='center', zorder=2, weight='bold')

    for i, team in enumerate(rb_rushing_df_parsed['team']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((rb_rushing_df_parsed['carries'] / weeks)[i], (rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (rb_rushing_df_parsed['carries'] / weeks).mean()
    y_mean = (rb_rushing_df_parsed['rushing_epa'] / rb_rushing_df_parsed['carries']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    plt.title(f'{formatted_date}: RB Carries per Game vs EPA per Carry', fontsize=16, fontweight='bold')
    plt.xlabel('Carries per Game', fontsize=12)
    plt.ylabel('EPA per Carry', fontsize=12)
    #save_fig(year, f'Player_RB_CPG_vs_EPAPC.png')
    plt.show()
    print('Player_RB_CPG_vs_EPAPC Completed')

def Player_WR_TPG_vs_EPAPT(df, weeks, year):   
    # Calibrateable thresholds for filtering WRs based on targets and receptions 
    tgts_threshold = 1*weeks
    #rec_threshold = 1*weeks
    
    wr_receiving_df_parsed = df[(df['targets'] > tgts_threshold) & (df['position'] == 'WR')]
    wr_receiving_df_parsed.reset_index(inplace=True)
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(wr_receiving_df_parsed['targets'] / weeks, wr_receiving_df_parsed['receiving_epa'] / wr_receiving_df_parsed['targets'], alpha=0.5, s=0)

    for index, row in wr_receiving_df_parsed.iterrows():
        plt.text(row['targets'] / weeks, (row['receiving_epa'] / row['targets']) + 0.25, row['player_name'], fontsize=9, ha='center', zorder=2, weight='bold')

    for i, team in enumerate(wr_receiving_df_parsed['team']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((wr_receiving_df_parsed['targets'] / weeks)[i], (wr_receiving_df_parsed['receiving_epa'] / wr_receiving_df_parsed['targets'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (wr_receiving_df_parsed['targets'] / weeks).mean()
    y_mean = (wr_receiving_df_parsed['receiving_epa'] / wr_receiving_df_parsed['targets']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    plt.title(f'{formatted_date}: WR Targets per Game vs EPA per Target', fontsize=16, fontweight='bold')
    plt.xlabel('Targets per Game', fontsize=12)
    plt.ylabel('EPA per Target', fontsize=12)
    #save_fig(year, f'Player_WR_TPG_vs_EPAPT.png')
    plt.show()
    print('Player_WR_TPG_vs_EPAPT Completed')

def Player_QB_CPOE_vs_EPA(df, weeks, year):   
    # Calibrateable thresholds
    completions_threshold = 2*weeks
    
    df_parsed = df[(df['completions'] > completions_threshold) & (df['position'] == 'QB')]
    df_parsed.reset_index(inplace=True)
        
    fig, ax = plt.subplots(figsize=(12,9))
    ax.scatter(df_parsed['passing_cpoe'], df_parsed['passing_epa'], alpha=0.5, s=0)

    for index, row in df_parsed.iterrows():
        plt.text(row['passing_cpoe'], row['passing_epa'] + 0.25, row['player_name'], fontsize=9, ha='center', zorder=2, weight='bold')

    for i, team in enumerate(df_parsed['team']):
        logo_url = get_team_logo(team)
        img = plt.imread(logo_url)
        imagebox = OffsetImage(img, zoom=0.02)
        ab = AnnotationBbox(imagebox, ((df_parsed['passing_cpoe'])[i], (df_parsed['passing_epa'])[i]), frameon=False,zorder=1)
        ax.add_artist(ab)

    x_mean = (df_parsed['passing_cpoe']).mean()
    y_mean = (df_parsed['passing_epa']).mean()
    ax.axvline(x=x_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))
    ax.axhline(y=y_mean, color='#290002', linestyle='--', linewidth=1, dashes=(5, 5))



    ax.grid(True, which='both', axis='both', linewidth=0.5, linestyle='--')

    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    plt.title(f'{formatted_date}: QB CPOE vs EPA', fontsize=16, fontweight='bold')
    plt.xlabel('CPOE', fontsize=12)
    plt.ylabel('EPA', fontsize=12)
    #save_fig(year, f'Player_QB_CPOE_vs_EPA.png')
    plt.show()
    print('Player_QB_CPOE_vs_EPA Completed')

if __name__ == '__main__':
    
    ### Load Data ###
    current_season = nfl.get_current_season()
    current_week = nfl.get_current_week()
    
    # Load current season play-by-play data
    pbp = nfl.load_pbp()
    # Load player game-level stats for multiple seasons
    player_stats = nfl.load_player_stats([current_season])
    # Load all available team level stats
    #team_stats = nfl.load_team_stats(seasons=True)
    team_stats = nfl.load_team_stats([current_season])
    
    
    # nflreadpy uses Polars instead of pandas. Convert to pandas if needed:
    pbp_pandas = pbp.to_pandas()
    player_stats_pandas = player_stats.to_pandas()
    team_stats_pandas = team_stats.to_pandas()
    
    
    ### Columns Check for Debugging ###
    team_stats_pandas.columns.to_list()
    cols_check = player_stats_pandas.columns.to_list()


    ### Season Stats ###
    player_stats_season_df = player_stats_season(player_stats_pandas)
    team_stats_season_df = team_stats_season(team_stats_pandas)
    
    ### Current Week Stats ###
    player_stats_current_week_df = player_stats_pandas[player_stats_pandas['week'] == current_week]
    team_stats_current_week_df = team_stats_pandas[team_stats_pandas['week'] == current_week]


    team_off_passing_df = team_off_passing(team_stats_pandas)
    
    
    ### Generate Plots ###
    Player_RB_CPG_vs_EPAPC(player_stats_season_df, current_week, current_season)
    Player_WR_TPG_vs_EPAPT(player_stats_season_df, current_week, current_season)
    Player_QB_CPOE_vs_EPA(player_stats_season_df, current_week, current_season)

    #Team_RushAtt_PassAtt_Off(team_stats_pandas, current_week, current_season)
    
    print('done')