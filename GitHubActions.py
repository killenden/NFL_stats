import sys
import stats
import os
from Sleeper import SleeperInfo

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
        weeks = week_number
        year = db_number
        nfl_state = SleeperInfo.get_nfl_state()
        year = nfl_state['season']
        weeks = nfl_state['week']
        print(f"Sleeper year received: {year}")
        print(f"Sleeper week received: {weeks}")
        db_dir = rf'database/{year}_database.db'
        current_directory = os.getcwd()
        db_dir = os.path.join(current_directory, db_dir)
        stats.Team_RushAtt_PassAtt_Off(db_dir, weeks, year)
        stats.Team_RushAtt_PassAtt_Off_Linearized(db_dir, weeks, year)
        stats.Team_RushAtt_PassAtt_Both(db_dir, weeks, year)
        stats.Team_RushAtt_PassAtt_Both_Linearized(db_dir, weeks, year)
        stats.Player_All_Passing_Target_Share(db_dir, weeks, year)
        stats.Player_WR_TPG_vs_YPR(db_dir, weeks, year)
        stats.Player_WR_RPG_vs_YPR(db_dir, weeks, year)
        stats.Player_WR_TPG_vs_RPG(db_dir, weeks, year)
        stats.Player_WR_RPG_vs_TDPR(db_dir, weeks, year)
        stats.Player_RB_YPG_vs_TDPG(db_dir, weeks, year)
        stats.Player_RB_YPG(db_dir, weeks, year)
        stats.Player_QB_Top12_1(db_dir, weeks, year)
        stats.Player_TE_TPG_vs_RPG(db_dir, weeks, year)
        stats.Player_QB_YPG_vs_TD(db_dir, weeks, year)
        stats.Player_QB_YPA_vs_CmpPct(db_dir,weeks)
        stats.Player_K_NetYards_vs_Touchback(db_dir,weeks)
        stats.Team_FFScoring_vs_Allowed_Def(db_dir, weeks, year)
        
    else:
        print("No DB number provided.")

if __name__ == "__main__":
    main()
