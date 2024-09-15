
def Passing(yards,td,two_pt,int):
    return yards * 0.04 + td * 4 + two_pt * 2 - int * 1

def Rushing(yards,td,two_pt):
    return yards * 0.1 + td * 6 + two_pt * 2 

def Receiving(recs,yards,td,two_pt):
    return recs * 1 + yards * 0.1 + td * 6 + two_pt * 2

def Kicking(FG_19,FG_29,FG_39,FG_49,FG_50,PAT,PAT_missed,FG_missed):
    return FG_19 * 3 + FG_29 * 3 + FG_39 * 3 + FG_49 * 4 + FG_50 * 5 + PAT - PAT_missed * 1 - FG_missed * 1

def Team_D(td, points_allowed, sacks, ints, fum_rec, safety, forced_fum, blocked_kick):
    points_allowed_pts = 0
    if points_allowed == 0:
        points_allowed_pts = 10
    elif points_allowed <= 6:
        points_allowed_pts = 7
    elif points_allowed <= 13:
        points_allowed_pts = 4
    elif points_allowed <= 20:
        points_allowed_pts = 1
    elif points_allowed <= 34:
        points_allowed_pts = -1
    else:
        points_allowed_pts = -4
    return td * 6 + points_allowed_pts + sacks * 1 + ints * 2 + fum_rec * 2 + safety * 2 + forced_fum * 1 + blocked_kick * 2

def Special_D(td,forced_fum,fum_rec):
    return td * 6 + forced_fum * 1 + fum_rec * 1

def Special_Player(td,forced_fum,fum_rec):
    return td * 6 + forced_fum * 1 + fum_rec * 1

def Misc(fum_lost, fum_rec_td):
    return -fum_lost * 2 + fum_rec_td * 6

#if __name__ == '__main__':
    
    # Josh_Allen = {'Pass_YD': 236,
    #               'Pass_TD': 1,
    #               'INT': 3,
    #               'Rush_YD': 36,
    #               'Fum_lost': 1
    #               }
    
    
    # points = Passing(Josh_Allen['Pass_YD'],Josh_Allen['Pass_TD'],0,Josh_Allen['INT'])
    # points += Rushing(Josh_Allen['Rush_YD'],0,0)
    # points += Misc(Josh_Allen['Fum_lost'], 0)
    # print(points)