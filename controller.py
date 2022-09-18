from fileinput import filename
from webbrowser import Opera
from html_scrape import HtmlScrape
from team import Team
from enum import Enum
from time import sleep
from tqdm import tqdm
from operation import Operation
from statistics import Statistic
from os import walk
import pandas as pd
import glob, os

class Controller:
    statistics = []

    def __init__(self, season):
        self.season = season
        self.html = HtmlScrape(season.value)
        self.html.connect()

        #self.start() 
        self.array_teams = []

    def start(self):
        self.a_hrefs = self.html.extract_teams() 
        
    def extract_team(self): 
        self.array_teams = []
        self.teams = [a_href for a_href in self.a_hrefs if '/squadre/' in str(a_href)]        
        for team in self.teams: 
            self.array_teams.append(Team(name = team.contents[0], scores = team.get("href"), season = self.season))
        
        self.array_teams.sort(key=lambda x: x.name) #ordinamento array per nome

    def get_stats(self, read): #ottengo statistiche 
        #il parametro read serve per leggere i csv con le statistiche (True) o fare scraping (False)
        print("Getting stats for each team...")
        if read: 
            self.read_season_csv()
            #df = pd.read_csv('data.csv')
        else:
            for team in tqdm(self.array_teams):
                team.get_scores()
                team.get_shots_for_match() 
        
    def save_stats(self):
        stat = Statistic(type = Operation.save_season_stats.value)

        print("Saving stats for each team...")
        for team in tqdm(self.array_teams):
            team.save_csv('/matches/')

        stat.stop_time()
        self.statistics.append(stat)

    def read_stats(self):
        filenames = next(walk(self.season.name+"/matches/"), (None, None, []))[2]  # tutti i file trovati nella cartella
        #file = self.season.name+"/stats/"+filenames[0]
        #df = pd.read_csv(file, index_col=0)
        for f in filenames:
            print(f)

    def read_season_csv(self): #legge i file per popolare la lista di squadre
        folder = self.season.name
        os.chdir(folder+'/shots/')
        for file in glob.glob("*.csv"):
            name = file.replace('.csv', '')
            team = Team(name=name, scores=None, season=folder)
            team.shot = pd.read_csv(file)
            team.match = pd.read_csv('../matches/'+file)

            self.array_teams.append(team)

    def merge_teams(self):
        for team in self.array_teams:
            team.merge_scores_shots()
        

        
class Season(Enum):
    Season20_21 = "https://fbref.com/it/comp/11/2020-2021/Statistiche-di-Serie-A-2020-2021"
    Season21_22 = "https://fbref.com/it/comp/11/2021-2022/Statistiche-di-Serie-A-2021-2022"
    Season22_23 = "https://fbref.com/it/comp/11/Statistiche-di-Serie-A"

controller = Controller(Season.Season21_22)
controller.read_season_csv()
controller.merge_teams()

#controller.extract_team()
#controller.get_stats(True)

#controller.save_stats()
#controller.read_stats()

