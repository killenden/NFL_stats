import sys
import stats
 
def main():
    if len(sys.argv) > 1:
        db_number = sys.argv[1]
        week_number = sys.argv[2]
        print(f"DB number received: {db_number}")
        print(f"week number received: {week_number}")
        db_name = rf'database\{db_number}_database.db'
        weeks = week_number
        stats.Team_Attempts(db_name)
        stats.Team_Attempts_Pct(db_name)
        stats.Team_Attempts_Both(db_name)
        stats.Team_Attempts_Both_Pct(db_name)
        stats.Target_Share(db_name)
        stats.TPG_vs_YPR(db_name, weeks)
        stats.RPG_YPG(db_name, weeks)
        stats.TPG_RPG(db_name, weeks)
        stats.RPG_vs_TDPR(db_name, weeks)
        stats.RB_YPG_vs_TDPG(db_name, weeks)
        stats.RB_YPG(db_name, weeks)
        stats.Top12QB(db_name, weeks)
        stats.Top12QB_1(db_name)
        
    else:
        print("No DB number provided.")

if __name__ == "__main__":
    main()
