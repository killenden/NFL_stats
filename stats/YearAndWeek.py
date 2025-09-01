from Sleeper import SleeperInfo
from datetime import datetime

def SetValue():
    nfl_state = SleeperInfo.get_nfl_state()
    if nfl_state['season_type'] == 'regular':
        year = nfl_state['season']
        weeks = nfl_state['week']
        print(f"Sleeper year received: {year}")
        print(f"Sleeper week received: {weeks}")
    else:
        year = datetime.now().year
        weeks = 1
        print(f"Sleeper season type is not regular, defaulting to year: {year} and weeks: {weeks}")
        

if __name__ == "__main__":
    SetValue()
