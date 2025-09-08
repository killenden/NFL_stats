import sys
import os
import ExecuteStats

def main():
    if len(sys.argv) > 1:
        year = sys.argv[1]
        weeks = sys.argv[2]
        try:
            weeks = int(weeks)
            print(f"Integer value: {weeks}")
        except ValueError:
            # If casting to int fails, try to cast to a float
            try:
                weeks = float(weeks)
                print(f"Float value: {weeks}")
            except ValueError:
                # If casting to float also fails, it's not a valid number
                print(f"Error: '{weeks}' is not a valid number")
        print(f"DB number received: {year}")
        print(f"week number received: {weeks}")
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        db_dir = os.path.join(base_dir, 'stats', 'database', f'{year}.db')
        
        
        ExecuteStats.Team_RushAtt_PassAtt_Off(db_dir, weeks, year)
        ExecuteStats.Team_RushAtt_PassAtt_Off_Linearized(db_dir, weeks, year)
        ExecuteStats.Team_RushAtt_PassAtt_Both(db_dir, weeks, year)
        ExecuteStats.Team_RushAtt_PassAtt_Both_Linearized(db_dir, weeks, year)
        ExecuteStats.Player_All_Passing_Target_Share(db_dir, weeks, year)
        ExecuteStats.Player_WR_TPG_vs_YPR(db_dir, weeks, year)
        ExecuteStats.Player_WR_RPG_vs_YPR(db_dir, weeks, year)
        ExecuteStats.Player_WR_TPG_vs_RPG(db_dir, weeks, year)
        ExecuteStats.Player_WR_RPG_vs_TDPR(db_dir, weeks, year)
        ExecuteStats.Player_RB_YPG_vs_TDPG(db_dir, weeks, year)
        ExecuteStats.Player_RB_YPG(db_dir, weeks, year)
        ExecuteStats.Player_QB_Top12_1(db_dir, weeks, year)
        ExecuteStats.Player_TE_TPG_vs_RPG(db_dir, weeks, year)
        ExecuteStats.Player_QB_YPG_vs_TD(db_dir, weeks, year)
        ExecuteStats.Player_QB_YPA_vs_CmpPct(db_dir,weeks, year)
        
    else:
        print("No DB number provided.")

if __name__ == "__main__":
    main()
