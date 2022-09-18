import requests
import pandas as pd
from bs4 import BeautifulSoup

class Team: 
    def __init__(self, name, scores, season):
        self.name = name
        self.link = f"https://fbref.com{scores}"
        self.season = season

    def get_scores(self): #ottiene i punteggi delle partite giocate
        self.data = requests.get(self.link)
        self.match = pd.read_html(self.data.text, match="Punteggi e partite")[0]
        self.dataset = self.match[self.match['Competizione'] == 'Serie A'] #filtro per Serie A, devo salvare solo la serie A, non mi interessa di Champions e altre partite
        
    def save_csv(self, folder): #salva il dataFrame in csv
        self.dataset.to_csv(self.season.name+folder+self.name+'.csv')

    def get_shots_for_match(self): #ottiene i tiri fatti in ciascuna partita giocata dalla squadra
        soup = BeautifulSoup(self.data.text, features="lxml")
        links = soup.find_all('a')
        
        links = [l.get("href") for l in links]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        
        data = requests.get(f"https://fbref.com{links[0]}")

        self.shot = pd.read_html(data.text, match="Tiri")[0]

        self.shot.columns = self.shot.columns.droplevel()
        self.dataset = self.shot[self.shot['Competizione'] == 'Serie A']
        #self.save_csv('/shots/')
        
    def merge_scores_shots(self):
        #self.dataset = pd.merge(self.match, self.shot, on = id, how='inner')
        #self.save_csv('/merge_stats_shots/')
        print("merge")
        #self.dataset = self.match.merge(self.shot[["Data", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")      
        #self.save_csv('/merge_stats_shots/')