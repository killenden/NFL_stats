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
            position_id INTEGER PRIMARY KEY,
            position_name TEXT NOT NULL
        );
        ''')
    
    cursor.executescript('''
        -- Example data for positions
        INSERT OR IGNORE INTO positions (position_name) VALUES
            ('Quarterback'),
            ('Running back'),
            ('Wide receiver'),
            ('Tight end'),
            ('Offensive lineman'),
            ('Defensive lineman'),
            ('Linebacker'),
            ('Cornerback'),
            ('Safety'),
            ('Kicker'),
            ('Punter');
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
            ('Jacksonville Jaguars', 'JAC', 'Jacksonville', 'Florida', 'AFC', 'South'),
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
            ('Washington Football Team', 'WAS', 'Landover', 'Maryland', 'NFC', 'East');
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

def get_team_id(db_file,team_name):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
        cursor.execute('SELECT team_id FROM teams WHERE shortname = ?', (team_name,))
        team_id = cursor.fetchone()[0]  # Assuming team_name is unique

        conn.close()
        return team_id

    except sqlite3.Error as e:
        print(f"Error retrieving team_id from SQLite database: {e}")
        return None
    
def get_player_id(team_name):
    try:
        conn = sqlite3.connect('teams.db')
        cursor = conn.cursor()

        # Assuming 'teams' table structure in 'teams.db' with id and team_name columns
        cursor.execute('''SELECT team_id FROM teams WHERE shortname = ?;''', (team_name))
        team_id = cursor.fetchone()[0]  # Assuming team_name is unique

        conn.close()
        return team_id

    except sqlite3.Error as e:
        print(f"Error retrieving team_id from SQLite database: {e}")
        return None

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