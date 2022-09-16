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


class Controller:
    statistics = []

    def __init__(self, season):
        self.season = season
        self.html = HtmlScrape(season.value)
        self.html.connect()

        self.start() 

    def start(self):
        self.a_hrefs = self.html.extract_teams() 
        
    def extract_team(self): 
        self.array_teams = []
        self.teams = [a_href for a_href in self.a_hrefs if '/squadre/' in str(a_href)]        
        for team in self.teams: 
            self.array_teams.append(Team(name = team.contents[0], scores = team.get("href"), season = self.season))
        
        self.array_teams.sort(key=lambda x: x.name) #ordinamento array per nome

    def get_stats(self):
        print("Getting stats for each team...")
        for team in tqdm(self.array_teams):
            team.get_scores()
        
    def save_stats(self):
        stat = Statistic(type = Operation.save_season_stats.value)

        print("Saving stats for each team...")
        for team in tqdm(self.array_teams):
            team.save_csv('/stats/')

        stat.stop_time()
        self.statistics.append(stat)

    def read_stats(self):
        filenames = next(walk(self.season.name+"/stats/"), (None, None, []))[2]  # tutti i file trovati nella cartella
        file = self.season.name+"/stats/"+filenames[0]
        df = pd.read_csv(file, index_col=0)
        
        
class Season(Enum):
    Season20_21 = "https://fbref.com/it/comp/11/2020-2021/Statistiche-di-Serie-A-2020-2021"
    Season21_22 = "https://fbref.com/it/comp/11/2021-2022/Statistiche-di-Serie-A-2021-2022"
    Season22_23 = "https://fbref.com/it/comp/11/Statistiche-di-Serie-A"

controller = Controller(Season.Season21_22)
controller.extract_team()
controller.get_stats()
#controller.save_stats()
#controller.read_stats()

