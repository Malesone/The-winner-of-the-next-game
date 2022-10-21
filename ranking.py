from gc import get_stats
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib
from tqdm import tqdm
from queue import Empty
from datetime import datetime
from pathlib import Path

class Ranking:
    def __init__(self, competition, season):
        self.competition = competition
        self.season = season
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


        years = self.season.split('-')
        self.year1, self.year2 = int(years[0]), int(years[1])

        self.all_previous_seasons_matches = {} 

    def download_matches(self, seasons):
        for i in range(seasons):        
            season = str(self.year1-(i+1))+'-'+str(self.year2-(i+1))
            page = 'https://fbref.com/it/comp/11/{}/calendario/Punteggi-e-partite-{}-Serie-A'.format(season, season)
            
            pageTree = requests.get(page)

            matches = pd.read_html(pageTree.text, match="Punteggi e partite")[0]
            columns = ['Casa', 'Ospiti', 'Punteggio']

            matches = matches[columns].dropna()
            matches.to_csv('files/'+self.competition+'/'+season+'.csv')
            self.all_previous_seasons_matches[i] = matches

    def download_season(self, season):
        page = 'https://fbref.com/it/comp/11/{}/calendario/Punteggi-e-partite-{}-Serie-A'.format(season, season)
        
        pageTree = requests.get(page)

        matches = pd.read_html(pageTree.text, match="Punteggi e partite")[0]
        columns = ['Casa', 'Punteggio', 'Ospiti']

        matches = matches[columns].dropna()
        matches.to_csv('files/'+self.competition+'/'+season+'.csv')
        self.all_previous_seasons_matches[len(self.all_previous_seasons_matches)] = matches

    def read_matches(self, seasons):
        for i in range(seasons):        
            season = str(self.year1-(i+1))+'-'+str(self.year2-(i+1))
            csv_file = Path('files/'+self.competition+'/'+season+'.csv')
        
            #se non trovo il file scarico i risultati 
            if csv_file.is_file() == False:
                self.download_season(season)
            
            matches = pd.read_csv('files/'+self.competition+'/'+season+'.csv', index_col=0)
            self.all_previous_seasons_matches[i] = matches

    def get_rank(self, team_name1, team_name2):
        team1, team2 = (0, 0)
        self.wins, self.loses, self.draws = 0, 0, 0
        for k, matches in self.all_previous_seasons_matches.items():
            teams = matches.Casa.unique()
            if team_name1 not in teams and team_name2 not in teams:
                team1, team2 = team1, team2 
            elif team_name1 not in teams and team_name2 in teams:
                team1, team2 = team1, team2 + 2
            elif team_name1 in teams and team_name2 not in teams:
                team1, team2 = team1 + 2, team2 
            else:
                v1, v2 = self.get_result(matches, team_name1, team_name2)
                team1, team2 = team1 + v1, team2 + v2

        return team1, team2

    def get_result(self, matches, t1, t2):
        team1, team2 = 0, 0
        matchdays = matches[((matches.Casa == t1) & (matches.Ospiti == t2)) | ((matches.Casa == t2) & (matches.Ospiti == t1))]
        matchdays = matchdays[['Casa','Punteggio','Ospiti']]

        for k, matchday in matchdays.iterrows():
            result = matchday.Punteggio.split('–')
            if t1 == matchday.Casa:
                if result[0] > result[1]:
                    self.wins += 1
                    team1 += 1
                elif result[0] < result[1]:
                    self.loses += 1
                    team2 += 1
                else:
                    self.draws += 1
            else:
                if result[0] > result[1]:
                    self.loses += 1
                    team2 += 1
                elif result[0] < result[1]:
                    self.wins += 1
                    team1 += 1
                else:
                    self.draws += 1
        return team1, team2

    def get_direct_stats(self):
        return self.wins, self.loses, self.draws
