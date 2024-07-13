import pandas as pd
import sqlite3

def pull_db(query,db_name):
    # Connect to your SQLite database
    conn = sqlite3.connect(db_name)  # Replace with your actual database file name


    # Execute the query and read the results into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()
    
    return df


def team_off_plays():
    db_name = r'database\2023_database.db'
    
    query = '''
    SELECT DISTINCT teams.team_name, teams.shortname, team_passing_off.Att AS Pass_Att, team_rushing_off.Att AS Rush_Att
    FROM teams
    INNER JOIN team_passing_off ON team_passing_off.Team = teams.team_id
    INNER JOIN team_rushing_off ON team_rushing_off.Team = teams.team_id;
    '''
    team_off_plays_df = pull_db(query,db_name)
    return team_off_plays_df

def team_def_plays():
    db_name = r'database\2023_database.db' 
    
    query = '''
    SELECT DISTINCT teams.team_name, teams.shortname, team_passing_def.Att AS Pass_Att, team_rushing_def.Att AS Rush_Att
    FROM teams
    INNER JOIN team_passing_def ON team_passing_def.Team = teams.team_id
    INNER JOIN team_rushing_def ON team_rushing_def.Team = teams.team_id;
    '''
    team_def_plays_df = pull_db(query,db_name)
    return team_def_plays_df
    

def team_both_plays():
    db_name = r'database\2023_database.db'
    
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

def team_off_target_share_plays():
    db_name = r'database\2023_database.db'
    
    query = '''
    SELECT DISTINCT players.Player, teams.shortname, team_passing_off.Att AS Pass_Off_Att, receiving.Tgts
    FROM players
    INNER JOIN teams ON teams.team_id = players.Team
    INNER JOIN team_passing_off ON team_passing_off.Team = players.Team
    INNER JOIN receiving ON receiving.Player = players.player_id;
    '''
    df = pull_db(query,db_name)
    return df





if __name__ == '__main__':
    
    #db_name = r'NFL_stats\database\2023_database.db'
    db_name = r'database\2023_database.db'
    
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