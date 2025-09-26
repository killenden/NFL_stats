import os
import YearAndWeek
import Processes.PullFromDatabase as PullFromDatabase
import FantasyCalculations.FantasyCalc


# Fantasy Football Scoring Settings

# Passing Stats
PASS_YARDS_PER_POINT = 25   # 1 point per 25 passing yards
PASS_TD_POINTS = 4          # 4 points per passing touchdown
INT_POINTS = -1             # -2 points per interception

# Rushing Stats
RUSH_YARDS_PER_POINT = 10   # 1 point per 10 rushing yards
RUSH_TD_POINTS = 6          # 6 points per rushing touchdown

# Receiving Stats
REC_YARDS_PER_POINT = 10    # 1 point per 10 receiving yards
REC_TD_POINTS = 6           # 6 points per receiving touchdown
RECEPTION_POINTS = 1        # 1 point per reception (PPR format)

# Miscellaneous
FUMBLE_LOST_POINTS = -2     # -2 points per fumble lost
TWO_POINT_CONVERSION = 2    # 2 points per two-point conversion
FG_0_39_POINTS = 3         # 3 points per field goal (0-39 yards)
FG_40_49_POINTS = 4        # 4 points per field goal (40-49 yards)
FG_50_PLUS_POINTS = 5       # 5 points per field goal (50+ yards)
PAT_POINTS = 1              # 1 point per extra point made
DEF_SACK_POINTS = 1         # 1 point per sack
DEF_INT_POINTS = 2          # 2 points per interception
DEF_FUMBLE_REC_POINTS = 2   # 2 points per fumble recovery
DEF_SAFETY_POINTS = 2       # 2 points per safety
DEF_TD_POINTS = 6           # 6 points per defensive/special teams touchdown
DEF_SHUTOUT_POINTS = 10     # 10 points for 0 points allowed
DEF_UNDER_7_POINTS = 7      # 7 points for under 7 points allowed
DEF_UNDER_14_POINTS = 4     # 4 points for under 14 points allowed

roster_settings = {
    'QB': 1,
    'RB': 2,
    'WR': 2,
    'TE': 1,
    'FLEX': 3,  # RB/WR/TE
    'SF': 1,    # QB/RB/WR/TE
}

teams = 12  # Number of teams in the league

def FFPointsCalc(db_name):
    ff_points_df = PullFromDatabase.ff_points(db_name)
    ff_points_df['FF_Points'] = ff_points_df['Pass TD']*PASS_TD_POINTS
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Pass Yds']/PASS_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Pass Int']*INT_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Fum']*FUMBLE_LOST_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rush Yds']/RUSH_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rush TD']*RUSH_TD_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec']*RECEPTION_POINTS)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec Yds']/REC_YARDS_PER_POINT)
    ff_points_df['FF_Points'] = ff_points_df['FF_Points']+(ff_points_df['Rec TD']*REC_TD_POINTS)
    return ff_points_df

def find_index(player_name, df):
    try:
        index = df.index[df['Player'] == player_name].tolist()[0]
        return index
    except IndexError:
        return None

def find_player(index, df):
    try:
        player_name = df.iloc[index]['Player']
        return player_name
    except IndexError:
        return None

def find_points(player_name, df):
    try:
        points = df.loc[df['Player'] == player_name, 'FF_Points'].values[0]
        return points
    except IndexError:
        return None
    
def get_pos(player_name, df):
    try:
        pos = df.loc[df['Player'] == player_name, 'POS'].values[0]
        return pos
    except IndexError:
        return None

def get_VORP(player, df):
    
    player_points = find_points(player, df)
    player_index = find_index(player, df)
    pos = get_pos(player, df)
    count = roster_settings.get(pos, 0) * teams
    
    flex = False
    superflex = False
    if pos == 'QB' or pos == 'WR' or pos == 'RB' or pos == 'TE':
        superflex = True
    elif pos == 'WR' or pos == 'RB' or pos == 'TE':
        flex = True


    pos_df = df[df['POS'] == pos].sort_values(by='FF_Points', ascending=False)
    pos_df.reset_index(drop=True, inplace=True)

    pos_replacement_index = (count - 1) - player_index
    pos_replacement_player = find_player(pos_replacement_index, pos_df)
    pos_replacement_point = find_points(pos_replacement_player, pos_df)
        
    if flex == True:
        flex_df = df[df['POS'].isin(['RB', 'WR', 'TE'])].sort_values(by='FF_Points', ascending=False)
        flex_df.reset_index(drop=True, inplace=True)
        
        flex_replacement_index = (count - 1) - player_index
        flex_replacement_player = find_player(flex_replacement_index, flex_df)
        flex_replacement_point = find_points(flex_replacement_player, flex_df)
        
    if superflex == True:
        sf_df = df[df['POS'].isin(['QB', 'RB', 'WR', 'TE'])].sort_values(by='FF_Points', ascending=False)
        sf_df.reset_index(drop=True, inplace=True)
        
        sf_replacement_index = (count - 1) - player_index
        sf_replacement_player = find_player(sf_replacement_index, sf_df)
        sf_replacement_point = find_points(sf_replacement_player, sf_df)
    
    replacement_point = max(pos_replacement_point, flex_replacement_point if flex else 0, sf_replacement_point if superflex else 0)
    replacement_player = pos_replacement_player if replacement_point == pos_replacement_point else (flex_replacement_player if flex and replacement_point == flex_replacement_point else sf_replacement_player)
        
    return {
        'Player': player,
        'POS': pos,
        'Player Points': player_points,
        'Replacement Player': replacement_player,
        'Replacement Points': replacement_point,
        'VORP': player_points - replacement_point
    }


if __name__ == '__main__':
    year, weeks = YearAndWeek.SetValue_Return()

    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    db_name = os.path.join(base_dir, 'stats', 'database', f'{year}.db')
    print(db_name)
    
    FF_points_df = FFPointsCalc(db_name)
    
    FF_points_all_df = FF_points_df.sort_values(by='FF_Points', ascending=False)
    FF_points_qb_df = FF_points_df[FF_points_df['POS'] == 'QB'].sort_values(by='FF_Points', ascending=False)
    FF_points_rb_df = FF_points_df[FF_points_df['POS'] == 'RB'].sort_values(by='FF_Points', ascending=False)
    FF_points_wr_df = FF_points_df[FF_points_df['POS'] == 'WR'].sort_values(by='FF_Points', ascending=False)
    FF_points_te_df = FF_points_df[FF_points_df['POS'] == 'TE'].sort_values(by='FF_Points', ascending=False)
    FF_points_flex_df = FF_points_df[FF_points_df['POS'].isin(['RB', 'WR', 'TE'])].sort_values(by='FF_Points', ascending=False)
    FF_points_sf_df = FF_points_df[FF_points_df['POS'].isin(['QB', 'RB', 'WR', 'TE'])].sort_values(by='FF_Points', ascending=False)

    FF_points_all_df.reset_index(drop=True, inplace=True)
    FF_points_qb_df.reset_index(drop=True, inplace=True)
    FF_points_rb_df.reset_index(drop=True, inplace=True)
    FF_points_wr_df.reset_index(drop=True, inplace=True)
    FF_points_te_df.reset_index(drop=True, inplace=True)
    FF_points_flex_df.reset_index(drop=True, inplace=True)
    FF_points_sf_df.reset_index(drop=True, inplace=True)

    starters = {pos: roster_settings.get(pos, 0) * teams for pos in roster_settings if pos != "FLEX" or pos != "SF" or pos != "BN"}
    flex_spots = roster_settings.get("FLEX", 0) * teams
    sf_spots = roster_settings.get("SF", 0) * teams
    #bench_spots = roster_settings.get("BN", 0) * teams
    
    test = get_VORP('Lamar Jackson', FF_points_all_df)

    print('done')
