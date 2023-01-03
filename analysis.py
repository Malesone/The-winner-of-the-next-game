import pandas as pd
import numpy as np 
from tqdm import tqdm
from team import Team
from datetime import datetime
import time
from sklearn.model_selection import train_test_split
from ranking import Ranking

class MatchAnalysis:
    rename_fields = {
        'Squadra': 'team1',
        'Avversario': 'team2',
        'Data': 'date',
        'Stadio': 'stadium',
        'Girone': 'matchday',
        'Risultato': 'result',
        'Rf': 'goals',
        'Tiri': 'total_shots',
        'Tiri.1': 'shots_on_target',
        'Rigori': 'goals_on_penalty',
        'Rig T': 'total_penalties',
        'Compl': 'completed_passings',
        'Tent': 'total_passings',
        'Angoli': 'corners',
        'Poss.': 'percentage_possession',
        'Falli': 'fouls',
        'Amm.': 'yellow_cards',
        'Esp.': 'red_cards',
    }

    def __init__(self):
        self.ranking = None

    def read_matches(self, path):
        self.matches_fe_team = pd.read_csv(path, index_col=0)
        self.matches_fe_team.reset_index(drop=True, inplace=True)

    def create_team_dataset(self):
        #for each team in the championship a dataset is created which contains all the games played by the team with the relative statistics
        self.matches_by_team = []
        self.matches_fe_team['date'] = pd.to_datetime(self.matches_fe_team['date'], format='%Y-%m-%d') 

        for number, team in enumerate(sorted(self.matches_fe_team.team1.unique())):
            self.matches_by_team.append(Team(number, team.lower(), self.matches_fe_team[self.matches_fe_team.team1 == team]))

    def divide_and_merge_home_away(self):
        #since the downloaded dataset contains information relating to the team's statistics, there will be 2 records for each match that refer to the same match: one record for the home team and one for the away team. I therefore divide who plays at home from who plays away by considering the "Stadio" field which precisely says whether the team plays at home or away (the team taken as a reference is the one on which the statistics are taken). Subsequently the 2 records that refer to the same game (one in the home_games dataset, one in the away_games dataset) are combined and in the end I obtain a dataset
        
        home_games = self.matches_fe_team[self.matches_fe_team.stadium =='Casa']
        away_games = self.matches_fe_team[self.matches_fe_team.stadium =='Ospiti']
        
        self.getDiff_home_away(home_games, away_games)

    def getDiff_home_away(self, hm, am):
        self.diff_dataset = []
        for index, home_match in hm.iterrows():
            away_match = am[(am['date'] == home_match['date']) & (am['team2'] == home_match['team1']) & (am['team1'] == home_match['team2'])]
            away_match_reduced = away_match.drop(columns = ['date', 'team1', 'team2', 'stadium', 'matchday', 'result', 'season'])
            for col in away_match_reduced.columns:
                home_match[col] = home_match[col] - away_match_reduced[col].values[0]

            self.diff_dataset.append(home_match)

        self.diff_dataset = pd.DataFrame(self.diff_dataset)
        
        self.diff_dataset.drop(columns=['stadium', 'matchday'], inplace=True)
        self.diff_dataset.sort_values(by=["date"], inplace=True)
        self.diff_dataset.reset_index(drop=True, inplace=True)

        self.diff_dataset.rename(columns={'team1':'home', 'team2': 'away'}, inplace=True)

    def readDiff_home_away(self):
        self.diff_dataset = pd.read_csv("files/diff_matches.csv", index_col=0)

    def reduce_dataset_with_avg(self, number, path):
        #I have to convert the type of the columns because the average between the values ​​gives me a number with a comma (from int to float)
        float_features_and_avg = [x for x in self.diff_dataset.columns if x != 'home' and x != 'away' and x != 'date' and x != 'result' and x != 'rank_h' and x != 'rank_a' and x != 'season']
        self.diff_dataset[float_features_and_avg] = self.diff_dataset[float_features_and_avg].astype(float)
        self.diff_dataset['date'] = pd.to_datetime(self.diff_dataset['date'], format='%Y-%m-%d') 

        for i, match_value in self.diff_dataset.iterrows():
            home, away = match_value.home, match_value.away
        
            averages_home, change1 = self.get_team_by_name(home).get_avg_last_X_matches(number, match_value.date, float_features_and_avg)
            averages_away, change2 = self.get_team_by_name(away).get_avg_last_X_matches(number, match_value.date, float_features_and_avg)
        
            if self.ranking != None:
                self.get_ranks(match_value, i)

            if change1 & change2: 
                for col in float_features_and_avg: 
                    diff = averages_home[col] - averages_away[col]
                    self.diff_dataset.at[i, col] = diff
        

        self.diff_dataset.home = self.diff_dataset.home.str.lower()
        self.diff_dataset.away = self.diff_dataset.away.str.lower()

        self.diff_dataset.to_csv(path)

    def merge_(self):
        self.features = [x for x in self.diff_dataset.columns if x != 'result']

        X, y = self.diff_dataset[self.features], self.diff_dataset.result.values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, shuffle=False) 

        self.set_codes()
    
    def set_ranking(self, ranking):
        self.ranking = ranking

    def get_ranks(self, match_value, pos):
        season = match_value.season.split('-')[1]
        team1, team2 = (0, 0)
        seasons_to_check = [x for x in sorted(self.ranking.all_previous_seasons_matches.keys()) if x <= int(season)]
        
        #for the rank I need the matches in the previous seasons, so I scan each season and add up the ranks
        for season_to_check in seasons_to_check: 
            matches = self.ranking.all_previous_seasons_matches[season_to_check] 
            teams = matches.Casa.unique()
            if match_value.home not in teams and match_value.away not in teams:
                team1, team2 = team1, team2 
            elif match_value.home not in teams and match_value.away in teams:
                team1, team2 = team1, team2 + 2
            elif match_value.home in teams and match_value.away not in teams:
                team1, team2 = team1 + 2, team2 
            else:
                v1, v2 = self.ranking.get_result(matches, match_value.home, match_value.away, match_value.date)

                team1 += v1
                team2 += v2
                
        self.diff_dataset.at[pos, 'rank_h'] = team1
        self.diff_dataset.at[pos, 'rank_a'] = team2

    def set_codes(self):
        for i, match_value in self.X_train.iterrows():
            self.X_train.at[i, 'home'] = self.get_team_code(match_value.home)
            self.X_train.at[i, 'away'] = self.get_team_code(match_value.away)
        
        for i, match_value in self.X_test.iterrows():
            self.X_test.at[i, 'home'] = self.get_team_code(match_value.home)
            self.X_test.at[i, 'away'] = self.get_team_code(match_value.away)

        self.X_train = self.X_train.drop(columns=['date'])
        self.X_test = self.X_test.drop(columns=['date'])

    def get_team_code(self, name): 
        for team in self.matches_by_team:
            if team.name == name:
                return team.id
    
    def get_name_by_id(self, id): 
        for team in self.matches_by_team:
            if team.id == id:
                return team.name
              
    def get_team_by_name(self, name):
        for team in self.matches_by_team:
            if team.name == name:
                return team

    def read_diff_dataset(self):
        self.diff_dataset = pd.read_csv("diff_with_ranking.csv", index_col=0)

    def get_id_by_name(self, name): 
        for team in self.matches_by_team:
            if team.name.upper() == name.upper():
                return team.id