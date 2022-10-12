from gc import get_stats
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import pathlib
from tqdm import tqdm
from queue import Empty
from datetime import datetime

class DownloadDati:
    """
    dizionario che contiene:
    * come chiave i nomi delle colonne trovati nei vari dataset
    * come valore i nuovi nomi delle colonne che verranno utilizzati nel codice
    """
    rename_fields = {
        'Squadra': 'team',
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
        self.set_util_hrefs() 

    def connect(self):
        headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        page = "https://fbref.com/it/comp/11/2021-2022/Statistiche-di-Serie-A-2021-2022"
        pageTree = requests.get(page)
        self.soup = BeautifulSoup(pageTree.text, features="lxml")

    def get_teams(self):
        table = self.soup.select('table.stats_table')[0]
        a_hrefs = table.find_all('a')
        self.teams = [a_href for a_href in a_hrefs if '/squadre/' in str(a_href)]        
        self.teams.sort(key=lambda x: x.contents[0]) #ordinamento per titolo
        
    def get_matches(self):
        self.datasets = pd.DataFrame()

        for team in self.teams:
            team_name = team.contents[0]
            link = f"https://fbref.com{team.get('href')}"
            data = requests.get(link)
            games = pd.read_html(data.text, match="Punteggi e partite")[0]

            matches = games[games['Competizione'] == self.competition]
            matches = matches[['Data', 'Girone', 'Stadio', 'Risultato', 'Rf', 'Avversario', 'Rs']]
 
            matches.insert(0, "Squadra", team_name)
 
            soup = BeautifulSoup(data.text, features="lxml")
            links = soup.find_all('a')
            href_links = [l.get("href") for l in links]

            self.get_stats_matches(matches, href_links)
    
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
        self.all_matches.to_csv("matches_fe_team.csv") #matches for each team
    
    def read_all_matches(self):
        self.all_matches = pd.read_csv("matches_fe_team.csv", index_col=0)

    def divide_and_merge_home_away(self):
        #dato che il dataset scaricato contiene le informazioni relative alle statistiche delle squadre, ci saranno per ogni partita 2 record che si riferiscono alla stessa partita: un record per la squadra di casa e uno per la squadra di trasferta. Divido quindi chi gioca in casa da chi gioca in trasferta andando a considerare il campo "Stadio" che dice appunto se la squadra gioca in casa o in trasferta (la squadra presa di riferimento è quella su cui vengono prese le statistiche). Successivamente i 2 record che si riferiscono alla stessa partita (uno nel dataset home_games, uno nel dataset away_games) vengono combinati ed alla fine ottengo un dataset 
        home_games = self.all_matches[self.all_matches['Stadio']=='Casa']
        away_games = self.all_matches[self.all_matches['Stadio']=='Ospiti']

        rename_home_fields = {key: 'h_'+value for key, value in self.rename_fields.items()}
        rename_home = rename_home_fields
        rename_home['Rs'] = 'a_goals'
        rename_home['Avversario'] = 'a_team'

        rename_away_fields = {key: 'a_'+value for key, value in self.rename_fields.items()}
        rename_away = rename_away_fields
        rename_away['Rs'] = 'h_goals'
        rename_away['Avversario'] = 'h_team'

        home_games = home_games.rename(columns=rename_home)
        away_games = away_games.rename(columns=rename_away)
        self.merge_home_away(home_games, away_games)

    def merge_home_away(self, home_games, away_games):
        merged_matches_by_home = pd.DataFrame()
        #il campo Data rimane così perché nel metodo precedente quando vengono rinominati i campi, per capire chi è home e chi away vengono messi due caratteri ("h_" per home e "a_" per away) all'inizio del campo e quindi con Data non ha senso fare h_date e a_date in quanto si riferiscano allo stesso dato
        away_columns_needed = ["a_team", "a_total_shots", "a_shots_on_target", "a_goals_on_penalty", "a_total_penalties", "a_corners", "a_yellow_cards", "a_red_cards", "a_fouls", "a_completed_passings",  "a_total_passings", "a_percentage_possession", "Data", "h_team"]

        for index, home_match in home_games.iterrows():
            away_match = away_games[(away_games['Data'] == home_match['Data']) & (away_games['h_team'] == home_match['h_team']) & (away_games['a_team'] == home_match['a_team'])]
            away_match_reduced = away_match[away_columns_needed]
            home_match = pd.merge(home_match.to_frame().T, away_match_reduced, on = ["Data", "h_team", "a_team"])
            merged_matches_by_home = merged_matches_by_home.append(home_match)    
    
        merged_matches_by_home['Data'] = pd.to_datetime(merged_matches_by_home['Data'], format='%d-%m-%Y')
        merged_matches_by_home = merged_matches_by_home.sort_values(by=['Data'], ascending=True)
        merged_matches_by_home = merged_matches_by_home.drop(columns=['Stadio'])

        merged_matches_by_home = merged_matches_by_home.rename(columns={"Data": "date", "Risultato": "result", 'Girone': 'matchday'})

        #tutte le informazioni necessarie per comporre il dataset
        columns_needed = ['h_team', 'h_goals', 'a_team', 'a_goals', 'result', 'date', 'matchday',
        'h_total_shots', 'h_shots_on_target', 'a_total_shots', 'a_shots_on_target', 
        'h_goals_on_penalty', 'h_total_penalties', 'a_goals_on_penalty', 'a_total_penalties', 
        'h_completed_passings', 'h_total_passings', 'a_completed_passings', 'a_total_passings',
        'h_corners', 'a_corners', 
        'h_fouls', 'h_yellow_cards', 'h_red_cards', 'a_yellow_cards', 'a_red_cards', 'a_fouls', 
        'h_percentage_possession', 'a_percentage_possession']
        
        merged_matches_by_home = merged_matches_by_home[columns_needed]
        merged_matches_by_home.insert(0, 'id', range(len(merged_matches_by_home)))
        merged_matches_by_home.to_csv("tournament.csv")

    def set_util_hrefs(self): 
        """il dizionario contiene:
        * come chiave parti di link contenuti in bottoni che permettono di creare dei link che portano ai vari dataset delle squadre 
        * come valori: 
            - il nome della sezione html che permette di accedere al dataset
            - le colonne utili da estrarre dai dataset per ottenere le statistiche utili
        """
        self.util_hrefs = {
            'all_comps/shooting/': {
                'section': 'Tiri',
                'columns': ['Data', 'Tiri','Tiri.1','Rigori','Rig T']
                },
            'all_comps/passing/': {
                'section': 'Passaggi',
                'columns': ['Data', 'Compl.', 'Tent,']
                },
                
            'all_comps/passing_types': {
                'section': 'Tipologie di passaggi',
                'columns': ['Data', 'Angoli']
                },
            'all_comps/possession': {
                'section': 'Possesso palla',
                'columns': ['Data', 'Poss.']
                },
            'all_comps/misc': {
                'section': 'Statistiche varie',
                'columns': ['Data', 'Falli', 'Amm.', 'Esp.']
                },
        }

