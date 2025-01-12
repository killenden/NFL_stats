import pandas as pd
import sqlite3
import os
import numpy as np


def pull_db(query,db_name):
    # Connect to your SQLite database
    conn = sqlite3.connect(db_name)  # Replace with your actual database file name

    # Execute the query and read the results into a DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Close the database connection
    conn.close()
    
    return df

def receiving(db_name):
    
    query = '''
    SELECT players.Player, positions.Pos, receiving.Type, receiving.Week, 
        SUM(receiving."Receiving Rec") AS "Rx Rec", 
        SUM(receiving."Receiving Yds") AS "Rx Yds", 
        AVG(CASE WHEN CAST(receiving."Receiving Avg" AS REAL) IS NOT NULL THEN CAST(receiving."Receiving Avg" AS REAL) ELSE NULL END) AS Avg, 
        MAX(CASE WHEN CAST(receiving."Receiving Lg" AS REAL) IS NOT NULL THEN CAST(receiving."Receiving Lg" AS REAL) ELSE NULL END) AS "Rx Lg", 
        SUM(receiving."Receiving TD") AS "Rx TD", 
        SUM(receiving."Receiving FD") AS "Rx FD", 
        SUM(receiving."Receiving 20+") AS "Rx twenty_plus", 
        SUM(receiving."Receiving Tar") AS "Rx Tgts", 
        SUM(receiving."Receiving YAC") AS "Rx YAC", 
        teams.team_name, 
        teams.shortname
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN receiving ON players.player_id = receiving.Player
    WHERE receiving.Type = 'Regular'
    GROUP BY players.Player;
    '''
    receiving_df = pull_db(query, db_name)
    return receiving_df

def rushing(db_name):
    query = '''
    SELECT DISTINCT 
        players.Player, 
        positions.POS, 
        rushing.Type, 
        rushing.Week, 
        SUM(rushing."Rushing Att") AS "Rush Att", 
        SUM(rushing."Rushing Yds") AS "Rush Yds", 
        AVG(CASE WHEN CAST(rushing."Rushing Avg" AS REAL) IS NOT NULL THEN CAST(rushing."Rushing Avg" AS REAL) ELSE NULL END) AS "Rush Avg", 
        MAX(CASE WHEN CAST(rushing."Rushing Lg" AS REAL) IS NOT NULL THEN CAST(rushing."Rushing Lg" AS REAL) ELSE NULL END) AS "Rush Lg", 
        SUM(rushing."Rushing TD") AS "Rush TD", 
        SUM(rushing."Rushing FD") AS "Rush FD", 
        SUM(rushing."Rushing 10+") AS "Rush ten_plus", 
        teams.team_name, 
        teams.shortname
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN rushing ON players.player_id = rushing.Player
    WHERE rushing.Type = 'Regular'
    GROUP BY players.Player;
    '''
    rushing_df = pull_db(query, db_name)
    #print(rushing_df.sort_values(by='TD', ascending=False))
    return rushing_df

def passing(db_name):
    query = '''
    SELECT DISTINCT 
        players.Player, 
        positions.POS, 
        passing.Type, 
        passing.Week, 
        SUM(passing."Passing Att") AS "Pass Att", 
        SUM(passing."Passing Cmp") AS "Pass Cmp",
        AVG(CASE WHEN CAST(passing."Passing YPA" AS REAL) IS NOT NULL THEN CAST(passing."Passing YPA" AS REAL) ELSE NULL END) AS "Pass YPA", 
        AVG(CASE WHEN CAST(passing."Passing Pct" AS REAL) IS NOT NULL THEN CAST(passing."Passing Pct" AS REAL) ELSE NULL END) AS "Pass Pct", 
        SUM(passing."Passing Yds") AS "Pass Yds", 
        SUM(passing."Passing TD") AS "Pass TD",
        AVG(CASE WHEN CAST(passing."Passing TD%T%" AS REAL) IS NOT NULL THEN CAST(passing."Passing TD%T%" AS REAL) ELSE NULL END) AS "Pass TD PCT", 
        SUM(passing."Passing Int") AS "Pass Int", 
        AVG(CASE WHEN CAST(passing."Passing Int%I%" AS REAL) IS NOT NULL THEN CAST(passing."Passing Int%I%" AS REAL) ELSE NULL END) AS "Pass INT PCT", 
        MAX(CASE WHEN CAST(passing."Passing Lg" AS REAL) IS NOT NULL THEN CAST(passing."Passing Lg" AS REAL) ELSE NULL END),
        SUM(passing."Passing FD") AS "Pass FD", 
        SUM(passing."Passing 20+") AS "Pass twenty_plus", 
        SUM(passing."Passing Sack") AS "Pass Sack", 
        AVG(CASE WHEN CAST(passing."Passing Loss" AS REAL) IS NOT NULL THEN CAST(passing."Passing Loss" AS REAL) ELSE NULL END) AS "Pass Loss",
        AVG(CASE WHEN CAST(passing."Passing Rate" AS REAL) IS NOT NULL THEN CAST(passing."Passing Rate" AS REAL) ELSE NULL END) AS "Pass Rate",
        teams.team_name, 
        teams.shortname
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN passing ON players.player_id = passing.Player
    WHERE passing.Type = 'Regular'
    GROUP BY players.Player;
    '''
    passing_df = pull_db(query, db_name)
    #print(passing_df.sort_values(by='TD', ascending=False))
    return passing_df

def qb(db_name):
    query = '''
    SELECT DISTINCT 
        players.Player, 
        positions.POS, 
        SUM(passing."Passing Yds") AS "Pass Yds", 
        AVG(CASE WHEN CAST(passing."Passing YPA" AS REAL) IS NOT NULL THEN CAST(passing."Passing YPA" AS REAL) ELSE NULL END) AS "Pass YPA", 
        SUM(passing."Passing Att") AS "Pass Att", 
        SUM(passing."Passing Cmp") AS "Pass Cmp", 
        SUM(passing."Passing TD") AS "Pass TD",
        SUM(passing."Passing Int") AS "Pass INT", 
        AVG(CASE WHEN CAST(passing."Passing Rate" AS REAL) IS NOT NULL THEN CAST(passing."Passing Rate" AS REAL) ELSE NULL END) AS "Pass Rate", 
        MAX(CASE WHEN CAST(passing."Passing Lg" AS REAL) IS NOT NULL THEN CAST(passing."Passing Lg" AS REAL) ELSE NULL END) AS "Pass Lg", 
        SUM(passing."Passing 20+") AS "Pass 20+",
        SUM(passing."Passing Sack") AS "Pass Sck", 
        SUM(passing."Passing Loss") AS "Pass SckY", 
        SUM(passing."Passing FD") AS "Pass FD", 
        SUM(rushing."Rushing Yds") AS "Rush Yds", 
        SUM(rushing."Rushing Att") AS "Rush Att", 
        SUM(rushing."Rushing TD") AS "Rush TD", 
        SUM(fumble."Fumbles Fum") AS "Fum", 
        SUM(rushing."Rushing FD") AS "Rush FD", 
        teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN passing ON players.player_id = passing.Player
    LEFT JOIN rushing ON players.player_id = rushing.Player
    LEFT JOIN fumble ON players.player_id = fumble.Player
    WHERE passing.Type = 'Regular'
    GROUP BY players.Player, positions.POS, teams.team_name;
    '''
    qb_df = pull_db(query, db_name)
    #print(qb_df)
    return qb_df

def fumble(db_name):
    query = '''
    SELECT DISTINCT 
        players.Player, 
        positions.POS, 
        fumble.Type, 
        fumble.Week, 
        SUM(fumble."Fumbles Fum"), 
        SUM(fumble."Fumbles Lost"), 
        SUM(fumble."Fumbles Forced"), 
        SUM(fumble."Recoveries Own"), 
        SUM(fumble."Recoveries Opp"), 
        SUM(fumble."Recoveries Tot"), 
        SUM(fumble."Returns Yds"), 
        SUM(fumble."Returns TD"), 
        teams.team_name, 
        teams.shortname
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN fumble ON players.player_id = fumble.Player
    WHERE fumble.Type = 'Regular'
    GROUP BY players.Player;
    '''
    fum_df = pull_db(query, db_name)
    #print(to_df)
    return fum_df

def team_def_downs(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_downs."First Downs Rush" AS "FD Rush", 
        defense_downs."First Downs Pass" AS "FD Pass", 
        defense_downs."First Downs Tot" AS "FD Tot", 
        defense_downs."Third Down Efficiency Att" AS "Third Down Att", 
        defense_downs."Third Down Efficiency Made" AS "Third Down Made", 
        defense_downs."Third Down Efficiency Pct" AS "Third Down Pct", 
        defense_downs."Fourth Down Efficiency Att" AS "Fourth Down Att", 
        defense_downs."Fourth Down Efficiency Made" AS "Fourth Down Made", 
        defense_downs."Fourth Down Efficiency Pct" AS "Fourth Down Pct"
    FROM teams
    INNER JOIN defense_downs ON defense_downs.Team = teams.team_id;
    '''
    team_def_downs_df = pull_db(query, db_name)
    return team_def_downs_df

def team_off_downs(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_downs."First Downs Rush" AS "FD Rush", 
        offense_downs."First Downs Pass" AS "FD Pass", 
        offense_downs."First Downs Tot" AS "FD Tot", 
        offense_downs."Third Down Efficiency Att" AS "Third Down Att", 
        offense_downs."Third Down Efficiency Made" AS "Third Down Made", 
        offense_downs."Third Down Efficiency Pct" AS "Third Down Pct", 
        offense_downs."Fourth Down Efficiency Att" AS "Fourth Down Att", 
        offense_downs."Fourth Down Efficiency Made" AS "Fourth Down Made", 
        offense_downs."Fourth Down Efficiency Pct" AS "Fourth Down Pct"
    FROM teams
    INNER JOIN offense_downs ON offense_downs.Team = teams.team_id;
    '''
    team_off_downs_df = pull_db(query, db_name)
    return team_off_downs_df

def team_def_kickoff_returns(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_kickoff_returns.Num, 
        defense_kickoff_returns.Yds, 
        defense_kickoff_returns.Avg, 
        defense_kickoff_returns.Lg, 
        defense_kickoff_returns.TD, 
        defense_kickoff_returns."Yds/G"
    FROM teams
    INNER JOIN defense_kickoff_returns ON defense_kickoff_returns.Team = teams.team_id;
    '''
    team_def_kickoff_returns_df = pull_db(query, db_name)
    return team_def_kickoff_returns_df

def team_off_kickoff_returns(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_kickoff_returns.Num, 
        offense_kickoff_returns.Yds, 
        offense_kickoff_returns.Avg, 
        offense_kickoff_returns.Lg, 
        offense_kickoff_returns.TD, 
        offense_kickoff_returns."Yds/G"
    FROM teams
    INNER JOIN offense_kickoff_returns ON offense_kickoff_returns.Team = teams.team_id;
    '''
    team_off_kickoff_returns_df = pull_db(query, db_name)
    return team_off_kickoff_returns_df

def team_def_overall(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_overall."Tot Pts" AS "Total Points", 
        defense_overall."Pts/G" AS "Points Per Game", 
        defense_overall."RushYds" AS "Rush Yards", 
        defense_overall."RYds/G" AS "Rush Yards Per Game", 
        defense_overall."PassYds" AS "Pass Yards", 
        defense_overall."PYds/G" AS "Pass Yards Per Game", 
        defense_overall."TotYds" AS "Total Yards", 
        defense_overall."Yds/G" AS "Total Yards Per Game"
    FROM teams
    INNER JOIN defense_overall ON defense_overall.Team = teams.team_id;
    '''
    team_def_overall_df = pull_db(query, db_name)
    return team_def_overall_df

def team_off_overall(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_overall."Tot Pts" AS "Total Points", 
        offense_overall."Pts/G" AS "Points Per Game", 
        offense_overall."RushYds" AS "Rush Yards", 
        offense_overall."RYds/G" AS "Rush Yards Per Game", 
        offense_overall."PassYds" AS "Pass Yards", 
        offense_overall."PYds/G" AS "Pass Yards Per Game", 
        offense_overall."TotYds" AS "Total Yards", 
        offense_overall."Yds/G" AS "Total Yards Per Game"
    FROM teams
    INNER JOIN offense_overall ON offense_overall.Team = teams.team_id;
    '''
    team_off_overall_df = pull_db(query, db_name)
    return team_off_overall_df

def team_def_passing(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_passing.Att AS "Pass Att", 
        defense_passing.Cmp AS "Pass Cmp", 
        defense_passing.Pct AS "Pass Pct", 
        defense_passing.Yds AS "Pass Yds", 
        defense_passing.YPA AS "Pass YPA", 
        defense_passing.TD AS "Pass TD", 
        defense_passing.Int AS "Pass Int", 
        defense_passing.Sack AS "Pass Sack", 
        defense_passing.Loss AS "Pass Loss", 
        defense_passing.Rate AS "Pass Rate", 
        defense_passing."NetYds" AS "Pass Net Yards", 
        defense_passing."Yds/G" AS "Pass Yards Per Game"
    FROM teams
    INNER JOIN defense_passing ON defense_passing.Team = teams.team_id;
    '''
    team_def_passing_df = pull_db(query, db_name)
    return team_def_passing_df

def team_off_passing(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_passing.Att AS "Pass Att", 
        offense_passing.Cmp AS "Pass Cmp", 
        offense_passing.Pct AS "Pass Pct", 
        offense_passing.Yds AS "Pass Yds", 
        offense_passing.YPA AS "Pass YPA", 
        offense_passing.TD AS "Pass TD", 
        offense_passing.Int AS "Pass Int", 
        offense_passing.Sack AS "Pass Sack", 
        offense_passing.Loss AS "Pass Loss", 
        offense_passing.Rate AS "Pass Rate", 
        offense_passing."NetYds" AS "Pass Net Yards", 
        offense_passing."Yds/G" AS "Pass Yards Per Game"
    FROM teams
    INNER JOIN offense_passing ON offense_passing.Team = teams.team_id;
    '''
    team_off_passing_df = pull_db(query, db_name)
    return team_off_passing_df

def team_def_rushing(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_rushing.Att AS "Rush Att", 
        defense_rushing.Yds AS "Rush Yds", 
        defense_rushing.Avg AS "Rush Avg", 
        defense_rushing.TD AS "Rush TD", 
        defense_rushing.FD AS "Rush FD", 
        defense_rushing."Yds/G" AS "Rush Yards Per Game"
    FROM teams
    INNER JOIN defense_rushing ON defense_rushing.Team = teams.team_id;
    '''
    team_def_rushing_df = pull_db(query, db_name)
    return team_def_rushing_df

def team_off_rushing(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_rushing.Att AS "Rush Att", 
        offense_rushing.Yds AS "Rush Yds", 
        offense_rushing.Avg AS "Rush Avg", 
        offense_rushing.TD AS "Rush TD", 
        offense_rushing.FD AS "Rush FD", 
        offense_rushing."Yds/G" AS "Rush Yards Per Game"
    FROM teams
    INNER JOIN offense_rushing ON offense_rushing.Team = teams.team_id;
    '''
    team_off_rushing_df = pull_db(query, db_name)
    return team_off_rushing_df

def team_def_scoring(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        defense_scoring."Touchdowns Tot" AS "Total TD", 
        defense_scoring."Touchdowns R" AS "Rush TD", 
        defense_scoring."Touchdowns P" AS "Pass TD", 
        defense_scoring."Touchdowns KR" AS "KR TD", 
        defense_scoring."Touchdowns IR" AS "IR TD", 
        defense_scoring."Touchdowns FR" AS "FR TD", 
        defense_scoring."Touchdowns BK" AS "BP TD", 
        defense_scoring."Touchdowns FGR" AS "FGR TD", 
        defense_scoring."Kicking PAT", 
        defense_scoring."Kicking FG", 
        defense_scoring."Misc Conv" AS "Conversions", 
        defense_scoring."Misc Saf" AS "Safety", 
        defense_scoring."Misc Pts" AS "Points"
    FROM teams
    INNER JOIN defense_scoring ON defense_scoring.Team = teams.team_id;
    '''
    team_def_scoring_df = pull_db(query, db_name)
    return team_def_scoring_df

def team_off_scoring(db_name):
    
    query = '''
    SELECT DISTINCT 
        teams.team_name, 
        teams.shortname, 
        offense_scoring."Touchdowns Tot" AS "Total TD", 
        offense_scoring."Touchdowns R" AS "Rush TD", 
        offense_scoring."Touchdowns P" AS "Pass TD", 
        offense_scoring."Touchdowns KR" AS "KR TD", 
        offense_scoring."Touchdowns IR" AS "IR TD", 
        offense_scoring."Touchdowns FR" AS "FR TD", 
        offense_scoring."Touchdowns BK" AS "BP TD", 
        offense_scoring."Touchdowns FGR" AS "FGR TD", 
        offense_scoring."Kicking PAT", 
        offense_scoring."Kicking FG", 
        offense_scoring."Misc Conv" AS "Conversions", 
        offense_scoring."Misc Saf" AS "Safety", 
        offense_scoring."Misc Pts" AS "Points"
    FROM teams
    INNER JOIN offense_scoring ON offense_scoring.Team = teams.team_id;
    '''
    team_off_scoring_df = pull_db(query, db_name)
    return team_off_scoring_df

def team_off_target_share_plays(db_name):
    
    query = '''
    SELECT DISTINCT 
        players.Player, 
        teams.shortname, 
        offense_passing.Att AS "Off Pass Att", 
        SUM(receiving."Receiving Tar") AS "Tgts"
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN offense_passing ON offense_passing.Team = players.Team
    INNER JOIN receiving ON receiving.Player = players.player_id
    WHERE receiving.Type = 'Regular'
    GROUP BY players.Player, teams.shortname;
    '''
    df = pull_db(query, db_name)
    return format_df(df)


def format_df(df):
    string_replace = ['Injured Reserve','Did Not Play','Inactive', '--']
    for i in df.columns:
        for j in string_replace:
            df[i] = df[i].replace(j,np.nan)
        if 'Lg' in i:
            for j in range(len(df[i])):
                if isinstance(df.loc[j, i], str):
                    df.loc[j, i] = int(df.loc[j, i].replace('t', df.loc[j, i][:-1]))
    return df

def total_stats(df):
    stat_dict = {}
    for player in df['Player'].unique():
        player_stats = []
        player_df = df[(df['Player'] == player) & (df['Type'] == 'Regular')]
        if len(player_df) == 0:
            continue
        for col in player_df.columns:
            if isinstance(player_df[col].values[0], str):
                continue
            else:
                player_stats.append((col, player_df[col].sum()))
        stat_dict[player] = player_stats
    return stat_dict

def process_stats(df):
    output_df = format_df(df)
    stat_dict = total_stats(output_df)
    return output_df, stat_dict

if __name__ == '__main__':
    
    #db_name = r'NFL_stats\database\2023_database.db'
    year = 2024
    db_name = rf'database\{year}.db'
    
    
    #df, stats = receiving(db_name)

    df = team_off_downs(db_name)
    
    
    
    query = '''
    SELECT players.Player, rushing.TD, teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN rushing ON players.player_id = rushing.Player
    ORDER BY rushing.TD DESC;
    '''
    rushing_TDs_df = pull_db(query,db_name)
    print(rushing_TDs_df.sort_values(by='TD', ascending=False))
    
    
    query = '''
    SELECT players.Player, positions.pos, passing."Pass Yds", passing."Yds/Att", passing."Att", passing."Cmp", passing."Cmp %", passing.TD as PassTD, rushing.TD as RushTD, rushing."Rush Yds" as RushYards, rushing."Rush FUM" as Fum, passing."INT", passing."Rate", passing."1st", passing."1st%", passing."20+", passing."40+", passing."Sck", passing."SckY", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    LEFT JOIN passing ON players.player_id = passing.Player
    LEFT JOIN rushing ON players.player_id = rushing.Player
    LEFT JOIN positions ON players.Pos = positions.pos_id
    WHERE positions.pos = 'QB';
    '''
    passing_TDs_df = pull_db(query,db_name)
    print(passing_TDs_df.sort_values(by='RushYards', ascending=True))
    
    query = '''
    SELECT players.Player, receiving.Rec, receiving.Tgts, receiving.TD, receiving.Yds, receiving."20+", receiving."40+", receiving."Rec FUM", receiving."Rec YAC/R", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN receiving ON players.player_id = receiving.Player;
    '''
    receiving_df = pull_db(query,db_name)
    print(receiving_df.sort_values(by='TD', ascending=False))
    
    
    #LEFT JOIN IS INCLUSIVE OFF ALL RESULTS
