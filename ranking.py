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
        
        years = self.season.split('-')
        self.year1, self.year2 = int(years[0]), int(years[1])
        
        self.all_previous_seasons_matches = {} 

    def download_matches(self, seasons, path):
        for i in range(seasons):        
            season = str(self.year1-(i+1))+'-'+str(self.year2-(i+1))
            page = 'https://fbref.com/it/comp/11/{}/calendario/Punteggi-e-partite-{}-Serie-A'.format(season, season)
            pageTree = requests.get(page)
            matches = pd.read_html(pageTree.text, match="Punteggi e partite")[0]
            columns = ['Data', 'Casa', 'Punteggio', 'Ospiti']
            matches = matches[columns].dropna()
             
            matches.Casa = matches.Casa.str.lower()
            matches.Ospiti = matches.Ospiti.str.lower()
            matches['Data'] = pd.to_datetime(matches['Data'], format='%d-%m-%Y') #I have to convert the date otherwise it gives me problems when i read it

            matches.to_csv(path.format(season))
            self.all_previous_seasons_matches[(self.year2-(i+1))] = matches

    def download_season(self, season, path, year):
        page = 'https://fbref.com/it/comp/11/{}/calendario/Punteggi-e-partite-{}-Serie-A'.format(season, season)
        pageTree = requests.get(page)
        matches = pd.read_html(pageTree.text, match="Punteggi e partite")[0]
        columns = ['Data', 'Casa', 'Punteggio', 'Ospiti']

        matches = matches[columns].dropna()
        matches.Casa = matches.Casa.str.lower()
        matches.Ospiti = matches.Ospiti.str.lower()

        matches['Data'] = pd.to_datetime(matches['Data'], format='%d-%m-%Y') #I have to convert the date otherwise it gives me problems when i read it

        matches.to_csv(path)
        self.all_previous_seasons_matches[year] = matches

    def read_matches(self, seasons, path):
        for i in range(seasons+1):        
            season = str(self.year1-i)+'-'+str(self.year2-i)
            csv_file = Path(path.format(season))
            #if I can't find the file, I download the results
            if csv_file.is_file() == False:
                self.download_season(season, path.format(season), (self.year2-i))

            matches = pd.read_csv(path.format(season), index_col=0)
            matches['Data'] = pd.to_datetime(matches['Data'], format='%Y-%m-%d') #I have to convert the date otherwise it gives me problems 
            self.all_previous_seasons_matches[(self.year2-i)] = matches

    def get_rank(self, team_name1, team_name2, date, season):
        team1, team2 = (0, 0)
        self.wins, self.loses, self.draws = 0, 0, 0
        
        seasons_to_check = [x for x in sorted(self.all_previous_seasons_matches.keys()) if x <= int(season)]
        
        #for the rank i need the matches in the previous seasonss
        for season_to_check in seasons_to_check: 
            matches = self.all_previous_seasons_matches[season_to_check] 
            matches = matches[matches.Data < date]
            
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

    def get_result(self, matches, t1, t2, date):
        team1, team2 = 0, 0
        matchdays = matches[((matches.Casa == t1) & (matches.Ospiti == t2)) | ((matches.Casa == t2) & (matches.Ospiti == t1))]
        matchdays = matchdays[matchdays.Data < date]
        
        if len(matchdays) != 0:    
            for i, single_match in matchdays.iterrows():
                result = single_match.Punteggio.replace('–','-').split('-')
                res = 'N'
                if int(result[0]) > int(result[1]):
                    res = 'V'
                elif int(result[0]) < int(result[1]):
                    res = 'P'

                if (((t1 == single_match.Casa) & (res == 'V')) | ((t1 == single_match.Ospiti) & (res == 'P'))):
                    team1 += 1 
                elif (((t2 == single_match.Casa) & (res == 'V')) | ((t2 == single_match.Ospiti) & (res == 'P'))):
                    team2 += 1 

        return team1, team2
