from gc import get_stats
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib
from tqdm import tqdm
from queue import Empty
from datetime import datetime
from IPython.display import display

class DownloadDati:
    """
    dizionario che contiene:
    * come chiave i nomi delle colonne trovati nei vari dataset
    * come valore i nuovi nomi delle colonne che verranno utilizzati nel codice
    """
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

    def __init__(self, competition):
        self.competition = competition

    def connect(self, page):
        #setta i parametri necessari alla connessione
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        pageTree = requests.get(page)
        self.soup = BeautifulSoup(pageTree.text, features="lxml")
        self.set_util_hrefs() 

    def get_teams_names(self):
        table = self.soup.select('table.stats_table')[0]
        a_hrefs = table.find_all('a')
        self.teams = [a_href for a_href in a_hrefs if '/squadre/' in str(a_href)]        
        self.teams.sort(key=lambda x: x.contents[0]) #ordinamento per titolo
        
    def get_matches(self):
        self.all_matches = pd.DataFrame()
        self.championship_games = pd.DataFrame()

        for team in self.teams:
            team_name = team.contents[0]
            link = f"https://fbref.com{team.get('href')}"
            data = requests.get(link)
            games = pd.read_html(data.text, match="Punteggi e partite")[0]

            matches = games[games['Competizione'] == self.competition]
            matches = matches[['Data', 'Girone', 'Stadio', 'Risultato', 'Rf', 'Avversario']]
 
            matches.insert(0, "Squadra", team_name)
 
            soup = BeautifulSoup(data.text, features="lxml")
            links = soup.find_all('a')
            href_links = [l.get("href") for l in links]

            matches = self.get_old_matches(matches)
            #ha senso prendere solo le partite che sono già state giocate, quelle con il risultato nullo (nan) significa che non sono ancora state giocate, quindi vengono "scartate"
            
            self.get_stats_matches(matches, href_links) 
            
    def get_old_matches(self, matches):
        matches.Risultato = matches.Risultato.astype(str)
        played_games = matches[matches.Risultato != 'nan']
        self.championship_games = self.championship_games.append(matches) 
        return played_games

    def get_stats_matches(self, matches, href_links):
        """
        per ciascuna squadra nella lista di squadre viene effettuato scraping dei vari dataset necessari per ottenere le statistiche di ciascun match
        """
        #la ricerca effettua il merge del dataset contenenti i match
        for href_key, section_value in self.util_hrefs.items():
            div_links = [l for l in href_links if l and href_key in l]
            html = requests.get(f"https://fbref.com{div_links[0]}")
            
            section, columns = section_value.items() #dal dizionario ottengo la sezione 
            section, columns = section[1], columns[1]

            #ottengo il dataset della pima sezione indicata nel match
            dataset_section = pd.read_html(html.text, match=section)[0]
            #elimino l'intestazione "Di: NomeSquadra"
            dataset_section.columns = dataset_section.columns.droplevel()
            #filtro il dataset per la competizione
            dataset_section = dataset_section[dataset_section['Competizione'] == self.competition]
            #filtro il dataset per le colonne selezionate
            dataset_section = dataset_section[[col for col in columns]]
            #print(dataset_section.columns)
            if section == 'Passaggi':
                column_names = dataset_section.columns.values
                column_names[1] = 'Compl'
                column_names[5] = 'Tent'
                dataset_section = dataset_section[['Data','Compl','Tent']]

            matches = pd.merge(matches, dataset_section, on = ["Data"])
            #matches.to_csv("../SerieA/Season21_22/Matches/"+team_name+".csv")

        self.all_matches = self.all_matches.append(matches) 
        
    def save_matches(self, path):
        """
        prima di salvare i match devono essere eseguite diverse operazioni: 
        * rinominazione dei campi
        * conversione data da stringa a datetime
        * ordinamento per data
        """
        self.all_matches.rename(columns=self.rename_fields, inplace=True)
        self.all_matches['date'] = pd.to_datetime(self.all_matches['date'], format='%d-%m-%Y') #devo convertire la data altrimenti mi dà problemi quando la lego         

        self.all_matches.sort_values(by=["date"], inplace=True)
        self.all_matches.to_csv(path) #matches for each team

    def save_championship_games(self, path):
        self.championship_games.rename(columns=self.rename_fields, inplace=True)
        self.championship_games = self.championship_games[self.championship_games.stadium=='Casa']
        self.championship_games['date'] = pd.to_datetime(self.championship_games['date'], format='%d-%m-%Y') #devo convertire la data altrimenti mi dà problemi quando la lego         
        self.championship_games.sort_values(by=["date"], inplace=True)
        self.championship_games.drop(columns=['stadium', 'goals'])
        self.championship_games.to_csv(path) #matches for each team

    def read_all_matches(self, path):
        self.all_matches = pd.read_csv(path, index_col=0)
        self.all_matches['date'] = pd.to_datetime(self.all_matches['date'], format='%d-%m-%Y')
    
    def set_util_hrefs(self): 
        """il dizionario contiene:
        * come chiave parti di link contenuti in bottoni che permettono di creare dei link che portano ai vari dataset delle squadre 
        * come valori: 
            - il nome della sezione html che permette di accedere al dataset
            - le colonne utili da estrarre dai dataset per ottenere le statistiche utili
        """
        #array = ['completed_passings','total_passings', 'corners']

        self.util_hrefs = {
            'all_comps/shooting/': {
                'section': 'Tiri',
                'columns': ['Data', 'Tiri','Tiri.1','Rigori','Rig T']
                },
            'all_comps/possession': {
                'section': 'Possesso palla',
                'columns': ['Data', 'Poss.']
                },
            'all_comps/misc': {
                'section': 'Statistiche varie',
                'columns': ['Data', 'Falli', 'Amm.', 'Esp.']
                }
            
        }
        """
        Vecchie sezioni che mi hanno fatto ottenere un'accuratezza minore
        'all_comps/passing/': {
            'section': 'Passaggi',
            'columns': ['Data', 'Compl.', 'Tent,']
            },
        'all_comps/passing_types': {
            'section': 'Tipologie di passaggi',
            'columns': ['Data', 'Angoli']
            },
        """

   