
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
import requests
import json

def get_user(username):
    r = requests.get('https://api.sleeper.app/v1/user/'+username)
    return json.loads(r.text)

def get_league(league_id):
    r = requests.get('https://api.sleeper.app/v1/league/'+league_id)
    return json.loads(r.text)

def get_league_rosters(league_id):
    r = requests.get('https://api.sleeper.app/v1/league/'+league_id+'/rosters')
    return json.loads(r.text)

def get_nfl_state():
    r = requests.get('https://api.sleeper.app/v1/state/nfl')
    return json.loads(r.text)



if __name__ == '__main__':
    year = 2024
    weeks = 9
    db_name = rf'database\{year}_database.db'
    username = 'killenden'
    league_id = '1115449767284281344'
    user_info = get_user(username)
    league_info = get_league(league_id)
    league_rosters = get_league_rosters(league_id)
    nfl_state = get_nfl_state()
    
    
    print('stop')
    
    
