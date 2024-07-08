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
            city TEXT,
            state TEXT,
            conference TEXT,
            division TEXT
        );

        -- Create table for players
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            team_id INTEGER,
            position TEXT,
            jersey_number INTEGER,
            height REAL,
            weight REAL,
            birthdate TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        );

        -- Create table for positions
        CREATE TABLE IF NOT EXISTS positions (
            position_id INTEGER PRIMARY KEY,
            position_name TEXT NOT NULL
        );

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

        -- Example data for teams
        INSERT OR IGNORE INTO teams (team_name, city, state, conference, division) VALUES
            ('Arizona Cardinals', 'Glendale', 'Arizona', 'NFC', 'West'),
            ('Atlanta Falcons', 'Atlanta', 'Georgia', 'NFC', 'South'),
            ('Baltimore Ravens', 'Baltimore', 'Maryland', 'AFC', 'North'),
            ('Buffalo Bills', 'Orchard Park', 'New York', 'AFC', 'East'),
            ('Carolina Panthers', 'Charlotte', 'North Carolina', 'NFC', 'South'),
            ('Chicago Bears', 'Chicago', 'Illinois', 'NFC', 'North'),
            ('Cincinnati Bengals', 'Cincinnati', 'Ohio', 'AFC', 'North'),
            ('Cleveland Browns', 'Cleveland', 'Ohio', 'AFC', 'North'),
            ('Dallas Cowboys', 'Dallas', 'Texas', 'NFC', 'East'),
            ('Denver Broncos', 'Denver', 'Colorado', 'AFC', 'West'),
            ('Detroit Lions', 'Detroit', 'Michigan', 'NFC', 'North'),
            ('Green Bay Packers', 'Green Bay', 'Wisconsin', 'NFC', 'North'),
            ('Houston Texans', 'Houston', 'Texas', 'AFC', 'South'),
            ('Indianapolis Colts', 'Indianapolis', 'Indiana', 'AFC', 'South'),
            ('Jacksonville Jaguars', 'Jacksonville', 'Florida', 'AFC', 'South'),
            ('Kansas City Chiefs', 'Kansas City', 'Missouri', 'AFC', 'West'),
            ('Las Vegas Raiders', 'Las Vegas', 'Nevada', 'AFC', 'West'),
            ('Los Angeles Chargers', 'Los Angeles', 'California', 'AFC', 'West'),
            ('Los Angeles Rams', 'Los Angeles', 'California', 'NFC', 'West'),
            ('Miami Dolphins', 'Miami Gardens', 'Florida', 'AFC', 'East'),
            ('Minnesota Vikings', 'Minneapolis', 'Minnesota', 'NFC', 'North'),
            ('New England Patriots', 'Foxborough', 'Massachusetts', 'AFC', 'East'),
            ('New Orleans Saints', 'New Orleans', 'Louisiana', 'NFC', 'South'),
            ('New York Giants', 'East Rutherford', 'New Jersey', 'NFC', 'East'),
            ('New York Jets', 'East Rutherford', 'New Jersey', 'AFC', 'East'),
            ('Philadelphia Eagles', 'Philadelphia', 'Pennsylvania', 'NFC', 'East'),
            ('Pittsburgh Steelers', 'Pittsburgh', 'Pennsylvania', 'AFC', 'North'),
            ('San Francisco 49ers', 'Santa Clara', 'California', 'NFC', 'West'),
            ('Seattle Seahawks', 'Seattle', 'Washington', 'NFC', 'West'),
            ('Tampa Bay Buccaneers', 'Tampa', 'Florida', 'NFC', 'South'),
            ('Tennessee Titans', 'Nashville', 'Tennessee', 'AFC', 'South'),
            ('Washington Football Team', 'Landover', 'Maryland', 'NFC', 'East');
    
        -- Example data for players (sample players for demonstration)
        INSERT OR IGNORE INTO players (player_name, team_id, position, jersey_number, height, weight, birthdate) VALUES
            ('Tom Brady', 23, 'Quarterback', 12, 6.4, 225, '1977-08-03'),
            ('Aaron Rodgers', 12, 'Quarterback', 12, 6.2, 225, '1983-12-02'),
            ('Patrick Mahomes', 16, 'Quarterback', 15, 6.3, 230, '1995-09-17'),
            ('Derrick Henry', 28, 'Running back', 22, 6.3, 247, '1994-01-04'),
            ('DeAndre Hopkins', 1, 'Wide receiver', 10, 6.1, 212, '1992-06-06'),
            ('Aaron Donald', 20, 'Defensive lineman', 99, 6.1, 280, '1991-05-23'),
            ('Jalen Ramsey', 20, 'Cornerback', 5, 6.1, 208, '1994-10-24');
''')
    
    
    
    # Commit changes and close connection
    conn.commit()
    conn.close()



def fetch_players_info(db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Fetch players' information with team details
    cursor.execute('''
        SELECT players.player_name, teams.team_name, players.position, players.jersey_number
        FROM players
        JOIN teams ON players.team_id = teams.team_id
    ''')
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Print the fetched data
    for row in rows:
        print(f"Player: {row[0]}, Team: {row[1]}, Position: {row[2]}, Jersey Number: {row[3]}")
    
    # Close connection
    conn.close()




# Create the database and populate it
#create_nfl_analytics_db(r'NFL_stats\database\2023_database.db')



# Example usage
fetch_players_info(r'NFL_stats\database\2023_database.db')