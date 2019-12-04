import numpy as np
import pandas as pd
import requests
import json
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

results_2017 = []
results_2018 = []
for game_id in range(2017020001, 2017021271, 1):
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/boxscore'.format(game_id)
    r_2017 = requests.get(url)
    game_data_2017 = r_2017.json()

    for homeaway in ['home','away']:

        game_dict_2017 = game_data_2017.get('teams').get(homeaway).get('teamStats').get('teamSkaterStats')
        game_dict_2017['team'] = game_data_2017.get('teams').get(homeaway).get('team').get('name')
        game_dict_2017['homeaway'] = homeaway
        game_dict_2017['game_id'] = game_id
        results_2017.append(game_dict_2017)

df_2017 = pd.DataFrame(results_2017)

for game_id in range(2018020001, 2018020667, 1):
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/boxscore'.format(game_id)
    r_2018 = requests.get(url)
    game_data_2018 = r_2018.json()

    for homeaway in ['home','away']:

        game_dict_2018 = game_data_2018.get('teams').get(homeaway).get('teamStats').get('teamSkaterStats')
        game_dict_2018['team'] = game_data_2018.get('teams').get(homeaway).get('team').get('name')
        game_dict_2018['homeaway'] = homeaway
        game_dict_2018['game_id'] = game_id
        results_2018.append(game_dict_2018)
        

df_2018 = pd.DataFrame(results_2018)

df = df_2017.append(df_2018)
is_home = df['homeaway_home'] == 1                                                                                                                                                                                                                   
home = df[is_home].drop('homeaway_away', axis=1).add_prefix('h_').rename(columns={'h_game_id':'game_id'})                                                                                                                                              
away = df[~is_home].drop(['Won/Lost', 'homeaway_home', 'homeaway_away'], axis=1).add_prefix('a_').rename(columns={'a_game_id':'game_id'})                                                                                                                       
df = pd.merge(home, away, on='game_id') 
df = df[['h_Won/Lost', 'h_blocked','h_faceOffWinPercentage', 'h_giveaways', 'h_goals', 'h_hits', 'h_pim',
        'h_powerPlayGoals', 'h_powerPlayOpportunities', 'h_powerPlayPercentage', 'h_shots', 'h_takeaways',
         
         'h_team_Anaheim Ducks', 'h_team_Arizona Coyotes',
         'h_team_Boston Bruins', 'h_team_Buffalo Sabres', 
         'h_team_Calgary Flames', 'h_team_Carolina Hurricanes', 'h_team_Chicago Blackhawks',
         'h_team_Colorado Avalanche', 'h_team_Columbus Blue Jackets',
         'h_team_Dallas Stars', 'h_team_Detroit Red Wings', 
         'h_team_Edmonton Oilers', 
         'h_team_Florida Panthers',
         'h_team_Los Angeles Kings',
         'h_team_Minnesota Wild', 'h_team_Montréal Canadiens',
         'h_team_Nashville Predators', 'h_team_New Jersey Devils',
         'h_team_New York Islanders', 'h_team_New York Rangers', 
         'h_team_Ottawa Senators',
         'h_team_Philadelphia Flyers', 'h_team_Pittsburgh Penguins', 
         'h_team_San Jose Sharks', 'h_team_St. Louis Blues', 
         'h_team_Tampa Bay Lightning', 'h_team_Toronto Maple Leafs', 
         'h_team_Vegas Golden Knights', 'h_team_Vancouver Canucks', 
         'h_team_Washington Capitals', 'h_team_Winnipeg Jets',
         
         'a_blocked','a_faceOffWinPercentage', 'a_giveaways', 'a_goals', 'a_hits', 'a_pim',
        'a_powerPlayGoals', 'a_powerPlayOpportunities', 'a_powerPlayPercentage', 'a_shots', 'a_takeaways',
         
         'a_team_Anaheim Ducks', 'a_team_Arizona Coyotes',
         'a_team_Boston Bruins', 'a_team_Buffalo Sabres', 
         'a_team_Calgary Flames', 'a_team_Carolina Hurricanes', 'a_team_Chicago Blackhawks',
         'a_team_Colorado Avalanche', 'a_team_Columbus Blue Jackets',
         'a_team_Dallas Stars', 'a_team_Detroit Red Wings', 
         'a_team_Edmonton Oilers', 
         'a_team_Florida Panthers',
         'a_team_Los Angeles Kings',
         'a_team_Minnesota Wild', 'a_team_Montréal Canadiens',
         'a_team_Nashville Predators', 'a_team_New Jersey Devils',
         'a_team_New York Islanders', 'a_team_New York Rangers', 
         'a_team_Ottawa Senators',
         'a_team_Philadelphia Flyers', 'a_team_Pittsburgh Penguins', 
         'a_team_San Jose Sharks', 'a_team_St. Louis Blues', 
         'a_team_Tampa Bay Lightning', 'a_team_Toronto Maple Leafs', 
         'a_team_Vegas Golden Knights', 'a_team_Vancouver Canucks', 
         'a_team_Washington Capitals', 'a_team_Winnipeg Jets'
        
        ]]
csv = df.to_csv('NHL_DATA_FULL.csv', index=False)