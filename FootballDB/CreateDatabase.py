import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Database
import utils

def check_csv_file(filename):
    """
    Check if a CSV file exists in the current directory.

    Parameters:
    - filename (str): Name of the CSV file to check.

    Returns:
    - bool: True if the CSV file exists, False otherwise.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, filename)  # Create file path

    if os.path.isfile(file_path) and filename.endswith('.csv'):
        return True
    else:
        return False

def create_db(year):
    db_name = rf'database\{year}.db' 
    
    print(os.path.dirname(os.path.realpath(__file__)))
    
    reset_db = input('Do you want to reset the db? This will delete all work. (y/n)   ')
    if reset_db == 'y':
        reset_db1 = input('Are you sure? (y/n)   ')
        if reset_db1 == 'y':
            Database.create_FootballDB_analytics_db(db_name)
    
    if (reset_db != 'y' or reset_db1 != 'y') and not os.path.exists(db_name):
        Database.create_FootballDB_analytics_db(db_name)
    
    filename = rf'database\{year}_temp_db'

    return filename, db_name

def reset_csv(filename):
    reset_csv_out = False
    reset_csv = input('Do you want to reset the rosters? (y/n)   ')
    if reset_csv == 'y':
        reset_csv1 = input('Are you sure? (y/n)   ')
        if reset_csv1 == 'y':
            reset_csv_out = True
            
    new_csv = False    
    if reset_csv_out == True or check_csv_file(filename+'.csv') == False:
        new_csv = True
        if check_csv_file(filename+'.csv') == True:
            current_dir = os.getcwd()  # Get current working directory
            file_path = os.path.join(current_dir, filename+'.csv')  # Create file path
            try:
                os.remove(file_path)
            except:
                pass
        file_path = None
            
    return new_csv