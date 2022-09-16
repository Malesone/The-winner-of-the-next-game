import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib

class HtmlScrape: 
    def __init__(self, season):
        self.season = season

    def connect(self): #connessione alla pagina principale di Serie A
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        page = self.season
        pageTree = requests.get(page)
        self.soup = BeautifulSoup(pageTree.text, features="lxml")

    def extract_teams(self): #estrazione dei dati dalla tabella con la classifica
        table = self.soup.select('table.stats_table')[0]
        a_hrefs = table.find_all('a')
        return a_hrefs

    def createFolders(self):
        # Directory
        directory = "teams/"
        # Parent Directory path
        parent_dir = pathlib.Path().resolve()

        for team in self.teams:
            new_directory = directory+team
            path = os.path.join(parent_dir, new_directory)
            os.mkdir(path)
