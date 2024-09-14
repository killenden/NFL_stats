import sys
import stats
import os
 
def main():
    if len(sys.argv) > 1:
        db_number = sys.argv[1]
        week_number = sys.argv[2]
        try:
            week_number = int(week_number)
            print(f"Integer value: {week_number}")
        except ValueError:
            # If casting to int fails, try to cast to a float
            try:
                week_number = float(week_number)
                print(f"Float value: {week_number}")
            except ValueError:
                # If casting to float also fails, it's not a valid number
                print(f"Error: '{week_number}' is not a valid number")
        print(f"DB number received: {db_number}")
        print(f"week number received: {week_number}")
        db_name = rf'database/{db_number}_database.db'
        current_directory = os.getcwd()
        db_dir = os.path.join(current_directory, db_name)
        weeks = week_number
        stats.Team_Attempts(db_dir)
        stats.Team_Attempts_Pct(db_dir)
        stats.Team_Attempts_Both(db_dir)
        stats.Team_Attempts_Both_Pct(db_dir)
        stats.Target_Share(db_dir)
        stats.TPG_vs_YPR(db_dir, weeks)
        stats.RPG_YPG(db_dir, weeks)
        stats.TPG_RPG(db_dir, weeks)
        stats.RPG_vs_TDPR(db_dir, weeks)
        stats.RB_YPG_vs_TDPG(db_dir, weeks)
        stats.RB_YPG(db_dir, weeks)
        stats.Top12QB(db_dir, weeks)
        stats.Top12QB_1(db_dir)
        
    else:
        print("No DB number provided.")

if __name__ == "__main__":
    main()
