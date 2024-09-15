import pandas as pd
import sqlite3
import os


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
    SELECT players.Player, positions.POS, receiving.Rec, receiving.Tgts, receiving.TD, receiving.Yds, receiving."20+", receiving."40+", receiving."Rec FUM", receiving."Rec YAC/R", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN receiving ON players.player_id = receiving.Player;
    '''
    receiving_df = pull_db(query,db_name)
    #print(receiving_df.sort_values(by='TD', ascending=False))
    return receiving_df

def rushing(db_name):
    query = '''
    SELECT DISTINCT players.Player, positions.POS, rushing."Rush Yds", rushing."Att", rushing."TD", rushing."Lng", rushing."20+", rushing."40+", rushing."Rush FUM", rushing."Rush 1st", rushing."Rush 1st%", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN rushing ON players.player_id = rushing.Player
    '''
    rushing_df = pull_db(query, db_name)
    #print(rushing_df.sort_values(by='TD', ascending=False))
    return rushing_df

def passing(db_name):
    query = '''
    SELECT DISTINCT players.Player, positions.POS, passing."Pass Yds", passing."Yds/Att", passing."Att", passing."Cmp", passing."Cmp %", passing."TD", passing."INT", passing."Rate", passing."Lng", passing."20+", passing."40+", passing."Sck", passing."SckY", passing."1st%", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN passing ON players.player_id = passing.Player
    '''
    passing_df = pull_db(query, db_name)
    #print(passing_df.sort_values(by='TD', ascending=False))
    return passing_df

def qb(db_name):
    query = '''
    SELECT DISTINCT players.Player, positions.POS, passing."Pass Yds", passing."Yds/Att", passing."Att", passing."Cmp", passing."TD" AS "Pass_TD", passing."INT", passing."Rate", passing."Lng", passing."20+", passing."40+", passing."Sck", passing."SckY", passing."1st%", rushing."Rush Yds", rushing."Att" AS "Rush_Att", rushing."TD" AS "Rush_TD", rushing."Rush FUM", rushing."Rush 1st", rushing."Rush 1st%", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    INNER JOIN positions ON players.Pos = positions.pos_id
    INNER JOIN passing ON players.player_id = passing.Player
    LEFT JOIN rushing ON players.player_id = rushing.Player
    '''
    qb_df = pull_db(query, db_name)
    #print(qb_df)
    return qb_df

def turnover(db_name):
    query = '''
    SELECT DISTINCT teams."shortname", team_fumbles_def."FR", team_ints_def."INT", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    LEFT JOIN team_fumbles_def ON teams.team_id = team_fumbles_def.Team
    LEFT JOIN team_ints_def ON teams.team_id = team_ints_def.Team
    '''
    to_df = pull_db(query, db_name)
    #print(to_df)
    return to_df

def tackles(db_name):
    query = '''
    SELECT DISTINCT teams."shortname", team_tackles_def."Comb", team_tackles_def."Asst", team_tackles_def."Solo", teams.team_name
    FROM players
    INNER JOIN teams ON players.Team = teams.team_id
    LEFT JOIN team_tackles_def ON teams.team_id = team_tackles_def.Team
    '''
    tackles_df = pull_db(query, db_name)
    #print(tackles_df)
    return tackles_df

def team_off_plays(db_name):
    
    query = '''
    SELECT DISTINCT teams.team_name, teams.shortname, team_passing_off.Att AS Pass_Att, team_rushing_off.Att AS Rush_Att
    FROM teams
    INNER JOIN team_passing_off ON team_passing_off.Team = teams.team_id
    INNER JOIN team_rushing_off ON team_rushing_off.Team = teams.team_id;
    '''
    team_off_plays_df = pull_db(query,db_name)
    return team_off_plays_df

def team_def_plays(db_name):
    
    query = '''
    SELECT DISTINCT teams.team_name, teams.shortname, team_passing_def.Att AS Pass_Att, team_rushing_def.Att AS Rush_Att
    FROM teams
    INNER JOIN team_passing_def ON team_passing_def.Team = teams.team_id
    INNER JOIN team_rushing_def ON team_rushing_def.Team = teams.team_id;
    '''
    team_def_plays_df = pull_db(query,db_name)
    return team_def_plays_df
    

def team_both_plays(db_name):
    
    query = '''
    SELECT DISTINCT teams.team_name, teams.shortname, team_passing_off.Att AS Pass_Off_Att, team_rushing_off.Att AS Rush_Off_Att, team_passing_def.Att AS Pass_Def_Att, team_rushing_def.Att AS Rush_Def_Att
    FROM teams
    INNER JOIN team_passing_off ON team_passing_off.Team = teams.team_id
    INNER JOIN team_rushing_off ON team_rushing_off.Team = teams.team_id
    INNER JOIN team_passing_def ON team_passing_def.Team = teams.team_id
    INNER JOIN team_rushing_def ON team_rushing_def.Team = teams.team_id;
    '''
    team_both_plays_df = pull_db(query,db_name)
    return team_both_plays_df

def team_off_target_share_plays(db_name):
    
    query = '''
    SELECT DISTINCT players.Player, teams.shortname, team_passing_off.Att AS Pass_Off_Att, receiving.Tgts
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN team_passing_off ON team_passing_off.Team = players.Team
    INNER JOIN receiving ON receiving.Player = players.player_id;
    '''
    df = pull_db(query,db_name)
    return df

def kickers(db_name):
    
    query = '''
    SELECT DISTINCT players.Player, teams.shortname, kickoff.KO, kickoff.Yds, kickoff."Ret Yds", kickoff.TB, kickoff."TB %", kickoff.Ret, kickoff.Ret_Avg
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN kickoff ON kickoff.Player = players.player_id;
    '''
    df = pull_db(query,db_name)
    return df

def fg_kickers(db_name):
    
    query = '''
    SELECT DISTINCT players.Player, teams.shortname, field_goal.FGM, field_goal.Att, field_goal."FG %", field_goal."1-19 > A-M", field_goal."20-29 > A-M", field_goal."30-39 > A-M", field_goal."40-49 > A-M", field_goal."50-59 > A-M", field_goal."50+ > A-M", field_goal."Lng", field_goal."Fg Blk"
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN field_goal ON field_goal.Player = players.player_id;
    '''
    df = pull_db(query,db_name)
    return df


def punters(db_name):
    
    query = '''
    SELECT DISTINCT players.Player, teams.shortname, punt.Avg, punt."Net Avg", punt."Net Yds", punt."Punts", punt."Lng", punt."Yds", punt."IN 20", punt."OOB", punt."Dn", punt."TB", punt."FC", punt."Ret", punt."Ret", punt."RetY", punt."TD", punt."P Blk"
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN punt ON punt.Player = players.player_id;
    '''
    df = pull_db(query,db_name)
    return df





if __name__ == '__main__':
    
    #db_name = r'NFL_stats\database\2023_database.db'
    year = 2020
    db_name = rf'database\{year}_database.db'
    
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
