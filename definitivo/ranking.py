from gc import get_stats
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib
from tqdm import tqdm
from queue import Empty
from datetime import datetime

class Ranking:
    def __init__(self, competition, season):
        self.competition = competition
        self.season = season
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    def download_matches(self, seasons):
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        self.all_previous_seasons_matches = {}

        years = self.season.split('-')
        year1, year2 = int(years[0]), int(years[1])
        
        for i in range(seasons):        
            season = str(year1-(i+1))+'-'+str(year2-(i+1))
            page = 'https://fbref.com/it/comp/11/{}/calendario/Punteggi-e-partite-{}-Serie-A'.format(season, season)
            
            pageTree = requests.get(page)

            matches = pd.read_html(pageTree.text, match="Punteggi e partite")[0]
            columns = ['Casa', 'Punteggio', 'Ospiti']

            matches = matches[columns].dropna()
            matches.to_csv('../'+self.competition+'/'+season+'.csv')
            self.all_previous_seasons_matches[i] = matches

    def get_rank(self, team_name1, team_name2):
        team1, team2 = (0, 0)
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
                    team1 += 1
                elif result[0] < result[1]:
                    team2 += 1
            else:
                if result[0] > result[1]:
                    team2 += 1
                elif result[0] < result[1]:
                    team1 += 1
        return team1, team2
