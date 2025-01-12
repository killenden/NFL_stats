import sqlite3

# Function to create database and tables
def create_nfl_analytics_db(db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.executescript('''
        -- Create table for teams
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL,
            shortname TEXT NOT NULL,
            city TEXT,
            state TEXT,
            conference TEXT,
            division TEXT
        );
        ''')

    cursor.executescript('''
        -- Create table for players
        CREATE TABLE IF NOT EXISTS players (
            jersey_number INTEGER,
            player_name TEXT NOT NULL,
            position TEXT,
            height REAL,
            weight REAL,
            birthdate TEXT,
            experience INTEGER,
            college TEXT,
            team_id INTEGER,
            player_id INTEGER PRIMARY KEY,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        );
        ''')
    
    cursor.executescript('''
        -- Create table for positions
        CREATE TABLE IF NOT EXISTS positions (
            POS TEXT NOT NULL,
            pos_id INTEGER PRIMARY KEY 
        );
        ''')

    
    cursor.executescript('''
        -- Example data for teams
        INSERT OR IGNORE INTO teams (team_name, shortname, city, state, conference, division) VALUES
            ('Arizona Cardinals', 'ARI', 'Glendale', 'Arizona', 'NFC', 'West'),
            ('Atlanta Falcons', 'ATL', 'Atlanta', 'Georgia', 'NFC', 'South'),
            ('Baltimore Ravens', 'BAL', 'Baltimore', 'Maryland', 'AFC', 'North'),
            ('Buffalo Bills', 'BUF', 'Orchard Park', 'New York', 'AFC', 'East'),
            ('Carolina Panthers', 'CAR', 'Charlotte', 'North Carolina', 'NFC', 'South'),
            ('Chicago Bears', 'CHI', 'Chicago', 'Illinois', 'NFC', 'North'),
            ('Cincinnati Bengals', 'CIN', 'Cincinnati', 'Ohio', 'AFC', 'North'),
            ('Cleveland Browns', 'CLE', 'Cleveland', 'Ohio', 'AFC', 'North'),
            ('Dallas Cowboys', 'DAL', 'Dallas', 'Texas', 'NFC', 'East'),
            ('Denver Broncos', 'DEN', 'Denver', 'Colorado', 'AFC', 'West'),
            ('Detroit Lions', 'DET', 'Detroit', 'Michigan', 'NFC', 'North'),
            ('Green Bay Packers', 'GB', 'Green Bay', 'Wisconsin', 'NFC', 'North'),
            ('Houston Texans', 'HOU', 'Houston', 'Texas', 'AFC', 'South'),
            ('Indianapolis Colts', 'IND', 'Indianapolis', 'Indiana', 'AFC', 'South'),
            ('Jacksonville Jaguars', 'JAX', 'Jacksonville', 'Florida', 'AFC', 'South'),
            ('Kansas City Chiefs', 'KC', 'Kansas City', 'Missouri', 'AFC', 'West'),
            ('Las Vegas Raiders', 'LV', 'Las Vegas', 'Nevada', 'AFC', 'West'),
            ('Los Angeles Chargers', 'LAC', 'Los Angeles', 'California', 'AFC', 'West'),
            ('Los Angeles Rams', 'LAR', 'Los Angeles', 'California', 'NFC', 'West'),
            ('Miami Dolphins', 'MIA', 'Miami Gardens', 'Florida', 'AFC', 'East'),
            ('Minnesota Vikings', 'MIN', 'Minneapolis', 'Minnesota', 'NFC', 'North'),
            ('New England Patriots', 'NE', 'Foxborough', 'Massachusetts', 'AFC', 'East'),
            ('New Orleans Saints', 'NO', 'New Orleans', 'Louisiana', 'NFC', 'South'),
            ('New York Giants', 'NYG', 'East Rutherford', 'New Jersey', 'NFC', 'East'),
            ('New York Jets', 'NYJ', 'East Rutherford', 'New Jersey', 'AFC', 'East'),
            ('Philadelphia Eagles', 'PHI', 'Philadelphia', 'Pennsylvania', 'NFC', 'East'),
            ('Pittsburgh Steelers', 'PIT', 'Pittsburgh', 'Pennsylvania', 'AFC', 'North'),
            ('San Francisco 49ers', 'SF', 'Santa Clara', 'California', 'NFC', 'West'),
            ('Seattle Seahawks', 'SEA', 'Seattle', 'Washington', 'NFC', 'West'),
            ('Tampa Bay Buccaneers', 'TB', 'Tampa', 'Florida', 'NFC', 'South'),
            ('Tennessee Titans', 'TEN', 'Nashville', 'Tennessee', 'AFC', 'South'),
            ('Washington Commanders', 'WSH', 'Landover', 'Maryland', 'NFC', 'East');
            ''')
    

    cursor.executescript('''
        -- Example data for teams
        INSERT OR IGNORE INTO positions (POS, pos_id) VALUES
        ('G', 1), ('WR', 2), ('LB', 3), ('S', 4), ('OT', 5), ('RB', 6), ('SAF', 7), ('LS', 8), ('C', 9), 
        ('CB', 10), ('DB', 11), ('DE', 12), ('P', 13), ('TE', 14), ('DT', 15), ('DL', 16), ('QB', 17), 
        ('K', 18), ('OLB', 19), ('OL', 20), ('FS', 21), ('NT', 22), ('FB', 23), ('ILB', 24), ('MLB', 25);
                ''')

    
    
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

def create_FootballDB_analytics_db(db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.executescript('''
        -- Create table for teams
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL,
            shortname TEXT NOT NULL,
            city TEXT,
            state TEXT,
            conference TEXT,
            division TEXT
        );
        ''')

    cursor.executescript('''
        -- Create table for players
        CREATE TABLE IF NOT EXISTS players (
            jersey_number INTEGER,
            player_name TEXT NOT NULL,
            position TEXT,
            height REAL,
            weight REAL,
            age TEXT,
            college TEXT,
            team_id INTEGER,
            player_id INTEGER PRIMARY KEY,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        );
        ''')
    
    cursor.executescript('''
        -- Create table for positions
        CREATE TABLE IF NOT EXISTS positions (
            POS TEXT NOT NULL,
            pos_id INTEGER PRIMARY KEY 
        );
        ''')

    
    cursor.executescript('''
        -- Example data for teams
        INSERT OR IGNORE INTO teams (team_name, shortname, city, state, conference, division) VALUES
            ('Arizona Cardinals', 'ARI', 'Glendale', 'Arizona', 'NFC', 'West'),
            ('Atlanta Falcons', 'ATL', 'Atlanta', 'Georgia', 'NFC', 'South'),
            ('Baltimore Ravens', 'BAL', 'Baltimore', 'Maryland', 'AFC', 'North'),
            ('Buffalo Bills', 'BUF', 'Orchard Park', 'New York', 'AFC', 'East'),
            ('Carolina Panthers', 'CAR', 'Charlotte', 'North Carolina', 'NFC', 'South'),
            ('Chicago Bears', 'CHI', 'Chicago', 'Illinois', 'NFC', 'North'),
            ('Cincinnati Bengals', 'CIN', 'Cincinnati', 'Ohio', 'AFC', 'North'),
            ('Cleveland Browns', 'CLE', 'Cleveland', 'Ohio', 'AFC', 'North'),
            ('Dallas Cowboys', 'DAL', 'Dallas', 'Texas', 'NFC', 'East'),
            ('Denver Broncos', 'DEN', 'Denver', 'Colorado', 'AFC', 'West'),
            ('Detroit Lions', 'DET', 'Detroit', 'Michigan', 'NFC', 'North'),
            ('Green Bay Packers', 'GB', 'Green Bay', 'Wisconsin', 'NFC', 'North'),
            ('Houston Texans', 'HOU', 'Houston', 'Texas', 'AFC', 'South'),
            ('Indianapolis Colts', 'IND', 'Indianapolis', 'Indiana', 'AFC', 'South'),
            ('Jacksonville Jaguars', 'JAX', 'Jacksonville', 'Florida', 'AFC', 'South'),
            ('Kansas City Chiefs', 'KC', 'Kansas City', 'Missouri', 'AFC', 'West'),
            ('Las Vegas Raiders', 'LV', 'Las Vegas', 'Nevada', 'AFC', 'West'),
            ('Los Angeles Chargers', 'LAC', 'Los Angeles', 'California', 'AFC', 'West'),
            ('Los Angeles Rams', 'LAR', 'Los Angeles', 'California', 'NFC', 'West'),
            ('Miami Dolphins', 'MIA', 'Miami Gardens', 'Florida', 'AFC', 'East'),
            ('Minnesota Vikings', 'MIN', 'Minneapolis', 'Minnesota', 'NFC', 'North'),
            ('New England Patriots', 'NE', 'Foxborough', 'Massachusetts', 'AFC', 'East'),
            ('New Orleans Saints', 'NO', 'New Orleans', 'Louisiana', 'NFC', 'South'),
            ('New York Giants', 'NYG', 'East Rutherford', 'New Jersey', 'NFC', 'East'),
            ('New York Jets', 'NYJ', 'East Rutherford', 'New Jersey', 'AFC', 'East'),
            ('Philadelphia Eagles', 'PHI', 'Philadelphia', 'Pennsylvania', 'NFC', 'East'),
            ('Pittsburgh Steelers', 'PIT', 'Pittsburgh', 'Pennsylvania', 'AFC', 'North'),
            ('San Francisco 49ers', 'SF', 'Santa Clara', 'California', 'NFC', 'West'),
            ('Seattle Seahawks', 'SEA', 'Seattle', 'Washington', 'NFC', 'West'),
            ('Tampa Bay Buccaneers', 'TB', 'Tampa', 'Florida', 'NFC', 'South'),
            ('Tennessee Titans', 'TEN', 'Nashville', 'Tennessee', 'AFC', 'South'),
            ('Washington Commanders', 'WSH', 'Landover', 'Maryland', 'NFC', 'East');
            ''')
    

    cursor.executescript('''
        -- Example data for teams
        INSERT OR IGNORE INTO positions (POS, pos_id) VALUES
        ('G', 1), ('WR', 2), ('LB', 3), ('S', 4), ('OT', 5), ('RB', 6), ('SAF', 7), ('LS', 8), ('C', 9), 
        ('CB', 10), ('DB', 11), ('DE', 12), ('P', 13), ('TE', 14), ('DT', 15), ('DL', 16), ('QB', 17), 
        ('K', 18), ('OLB', 19), ('OL', 20), ('FS', 21), ('NT', 22), ('FB', 23), ('ILB', 24), ('MLB', 25);
                ''')

    
    
    
    # Commit changes and close connection
    conn.commit()
    conn.close()



def add_players_info(db_file,df):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    df.to_sql('players', conn, if_exists='replace', index=False)
    
    conn.close()
    
def add_team_info(db_file,df):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    df.to_sql('players', conn, if_exists='replace', index=False)
    
    conn.close()


def get_pos_id(db_file,pos_name):
    import numpy as np
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
        try:
            cursor.execute('SELECT pos_id FROM positions WHERE POS = ?', (pos_name,))
            pos_id = cursor.fetchone()[0]  # Assuming team_name is unique
        except:
            pos_id = np.nan

        conn.close()
        return pos_id

    except sqlite3.Error as e:
        print(f"Error retrieving pos_id from SQLite database: {e}")
        return None

def get_team_id(db_file,team_name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
        try:
            cursor.execute('SELECT team_id FROM teams WHERE team_name = ?', (team_name,))
            team_id = cursor.fetchone()[0]  # Assuming team_name is unique
        except:
            import numpy as np
            team_id = max(cursor.execute('SELECT team_id FROM teams').fetchall())[0] + 1
            data = [(team_id, team_name, team_name[0]+str(team_id), np.nan,np.nan,np.nan,np.nan),]
            cursor.executemany("INSERT INTO teams VALUES(?, ?, ?, ?, ?, ?, ?)", data)
            conn.commit()  # Remember to commit the transaction after executing INSERT.
        

        conn.close()
        return team_id

    except sqlite3.Error as e:
        print(f"Error retrieving team_id from SQLite database: {e}")
        return None
    
def get_team_id_shortname(db_file,team_name1):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
            cursor.execute('SELECT team_id FROM teams WHERE shortname = ?', (team_name1,))
            team_id = cursor.fetchone()[0]  # Assuming team_name is unique
        except:
            try:
                cursor.execute("SELECT team_id FROM teams WHERE team_name LIKE ?", ('%'+team_name1+'%',))
                team_id = cursor.fetchone()[0]  # Assuming team_name is unique
            except:
                import numpy as np
                team_id = max(cursor.execute('SELECT team_id FROM teams').fetchall())[0] + 1
                data = [(team_id, team_name1, team_name1[0]+str(team_id), np.nan,np.nan,np.nan,np.nan),]
                cursor.executemany("INSERT INTO teams VALUES(?, ?, ?, ?, ?, ?, ?)", data)
                conn.commit()  # Remember to commit the transaction after executing INSERT.
        

        conn.close()
        return team_id

    except sqlite3.Error as e:
        print(f"Error retrieving team_id from SQLite database: {e}")
        return None
    
def get_player_id(db_file,players):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
        try:
            cursor.execute('SELECT player_id FROM players WHERE Player = ?', (players,))
            player_id = cursor.fetchone()[0]  # Assuming team_name is unique
        except:
            player_id = ''
        conn.close()
        return player_id

    except sqlite3.Error as e:
        print(f"Error retrieving player_id from SQLite database: {e}")
        return None
    
    
def datatypes(df):
    import utils
    
    dtype = {}
    
    for column in df.columns:
        value = df[column].iloc[0]
        format = type(utils.string_to_float(value))
        if format is str:
            dict_value = 'TEXT'
        elif format is int:
            dict_value = 'INTEGER'
        elif format is float:
            dict_value = 'REAL'
        dtype[column] = dict_value
    
    return dtype
    
def add_database_information(table_name,db_file,df,dtypes):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    #TODO: Make this work! Do a for loop across the columns for the keys and the first row for the values. Then use something like utils.string_to_float to check if it is a float or not
    # Could also just do type()
    
    # dtype = {
    # 'Player': 'TEXT',
    # 'TD': 'INTEGER',
    # 'team_name': 'TEXT',
    # 'score': 'REAL'  # Specify as REAL (floating point)
    # }
    
    df.to_sql(table_name, conn, if_exists='replace', index=False, dtype=dtypes)
    #df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.close()

# def fetch_players_info(db_file):
#     # Connect to SQLite database
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
    
#     # Fetch players' information with team details
#     cursor.execute('''
#         SELECT players.player_name, teams.team_name, players.position, players.jersey_number
#         FROM players
#         JOIN teams ON players.team_id = teams.team_id
#     ''')
    
#     # Fetch all rows
#     rows = cursor.fetchall()
    
#     # Print the fetched data
#     for row in rows:
#         print(f"Player: {row[0]}, Team: {row[1]}, Position: {row[2]}, Jersey Number: {row[3]}")
    
#     # Close connection
#     conn.close()




# Create the database and populate it
#create_nfl_analytics_db(r'NFL_stats\database\2023_database.db')



# Example usage
#fetch_players_info(r'NFL_stats\database\2023_database.db')