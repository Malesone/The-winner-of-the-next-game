import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib

class HtmlScrape: 
    def connect(self):
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        page = "https://fbref.com/it/comp/11/Statistiche-di-Serie-A"
        pageTree = requests.get(page)
        self.soup = BeautifulSoup(pageTree.text, features="lxml")

    def extract_teams(self):
        table = self.soup.select('table.stats_table')[0]
        a_hrefs = table.find_all('a')
        return a_hrefs
        
    def searchLink(self):
        team_urls = [f"https://fbref.com{l}" for l in self.links]
        #for team_url in team_urls: 
        data = requests.get(team_urls[0])
        matches = pd.read_html(data.text, match="Punteggi e partite")[0]
        print(matches)
        

    def createFolders(self):
        # Directory
        directory = "teams/"
        # Parent Directory path
        parent_dir = pathlib.Path().resolve()

        for team in self.teams:
            new_directory = directory+team
            path = os.path.join(parent_dir, new_directory)
            os.mkdir(path)

