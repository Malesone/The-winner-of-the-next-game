from operator import index
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from difflib import SequenceMatcher
import numpy as np

class FootballPredictions:
    def __init__(self, matches):
        self.football_predictions_link = 'https://footballpredictions.com/footballpredictions/?date='
        self.format_date = '%d-%m-%Y'
        self.headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        self.matches = matches[['home', 'away', 'date']]
        self.originalNotation = sorted(self.matches.home.unique())

    def add_awayNotation(self):
        aways = sorted(self.matches.away.unique())
        self.originalNotation.append(aways)
        self.originalNotation = self.flatten(self.originalNotation)

    def flatten(self, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])

### INIZIO ___________ GESTIONE URL PER DATA
    def get_urls(self):
        #permette di ottenere tutti i link che portano alla pagina contenente le partite di un determinato giorno. Il giorno viene settato nel link
        #ho notato che i link relativi alle news di Serie A contengono la parola serieapredictions, quindi ottengo tutti i link e poi filtro per quelli contenente la parola

        match_dates = self.matches.date.unique()

        urls = {}
        for date in match_dates:
            page = self.football_predictions_link
            string_data = date
            converted_data = pd.to_datetime(string_data, format='%Y-%m-%d', errors='coerce').date()
            link_data = converted_data.strftime(self.format_date)
            page += link_data
            urls[str(converted_data)] = page


        #ho notato che i link relativi alle news contengono la parola serieapredictions, quindi ottengo tutti i link e poi filtro per quelli contenente la parola.
        #quello che vado a fare è creare un dizionario dove come chiave ho la data del match, mentre come valore ho un array di link che portano a pagine contenenti le news e predizioni delle squadre coinvolte nel match
        self.links_of_pages_by_date = {}
        for key, link_page in tqdm(urls.items()):
            pageTree = requests.get(link_page)
            soup = BeautifulSoup(pageTree.text, features="lxml")
            links = soup.find_all('a', href=True)
            links = [link['href'] for link in links if 'serieapredictions' in link['href']]
            cleaned_links = list(dict.fromkeys(links))
            cleaned_links.pop(0)
            self.links_of_pages_by_date[key] = cleaned_links

    def save_urls(self):
        with open("files/keyDat_valueLinks.json", "w") as fp:
            json.dump(self.links_of_pages_by_date,fp, indent=4) 

    def read_urls(self):
        file_links = open('../files/keyDat_valueLinks.json')  
        self.links_of_pages_by_date = json.load(file_links)
        file_links.close()
### FINE ___________ GESTIONE URL PER DATA
    
### INIZIO ___________ DOWNLOAD PREDIZIONI
    def get_predictions(self):
        self.df = pd.DataFrame()
        count = 0
        for key_date, links_of_predictions in tqdm(self.links_of_pages_by_date.items()):
            for prediction_link in links_of_predictions:
                home, away, details, label = self.get_prediction(prediction_link)
                self.df.at[count, 'date'] = key_date        
                self.df.at[count, 'home'] = self.check_name(home)
                self.df.at[count, 'away'] = self.check_name(away)
                
                details = '\n\n'.join(details)
                self.df.at[count, 'description'] = details
                self.df.at[count, 'prediction'] = label
                
                count += 1

        #dato che il procedimento di scaricamento delle descrizioni è molto lungo, tutti i dati sono salvati nel seguente csv. Il problema è che i dati devono essere elaborati, quindi guardare le sezioni successive
        self.df.to_csv("files/all_descriptive_prediction.csv")

    def get_prediction(self, prediction_link):
        """
        get_prediction è il metodo che permette di ottenere 3 dati: 
        - il nome della squadra di casa
        - il nome della squadra di trasferta
        - la predizione (descrizione)
        """
        pageTree = requests.get(prediction_link)
        soup = BeautifulSoup(pageTree.text, features="lxml")
        #vado a prendere il div contenente le predizioni
        predtxt = soup.find("div", {"class": "predictiontxt"})
        details = []
        paragraph = predtxt.find_all('p')
        for p in paragraph:
            #in un aggiornamento della pagina, hanno messo anche "This match will be played" + data. Non mi interessa per la predizione, quindi lo scarto. In più ha senso considerare solo paragrafi che hanno del testo. Per alcune partite c'è anche la stringa "This prediction will be released soon." 
            p_text = p.text
            if ("This match will be played" not in p_text) & (len(p_text) > 0) & ("This prediction will be released soon." not in p_text): 
                details.append(p.text)

        #ottengo i nomi delle squadre che si affrontano
        paragraph_team = soup.find_all("p", {"class": "teamnaam"})

        #cerco il risultato predetto
        predbox = soup.find("div", {"class": "predictionbox"})
        predictions = predbox.find("strong").text.split('-')
        
        return paragraph_team[0].contents[0], paragraph_team[1].contents[0], details, self.get_label(predictions, predbox)
 
    def check_name(self, new_name):
        """
        I nomi delle squadre che vengono letti da football predictions non sono normalizzati quindi bisogna cambiare il nome.

        Prendo i nomi delle squadre salvate sul file dei risultati e prendo il nome della squadra prese da football predictions. Se trovo la corrispondenza, converto il nome della squadra, altrimenti lascio il nome attuale.

        Ho visto che ad esempio invece di scrivere Cagliari, è stato scritto Calgiari. Controllo la percentuale di similarità tra le due stringhe e se varia di una lettera, lo score sarà alto (maggiore di 0.8 --> 0.857 per l'esattezza)
        """
        
        for team_name in self.originalNotation:
            if (team_name in new_name) or (new_name in team_name) or (SequenceMatcher(None, new_name, team_name).ratio() > 0.8): 
                return team_name
        return new_name

    def get_label(self, predictions, predbox):
        #ritorna la classe di predizione del match in base alla squadra di home (V = vittoria home, P = sconfitta home, N = pareggio)
        if len(predictions) > 1:
            home_goals, away_goals = predbox.find("strong").text.split('-')
            home_goals = int(home_goals)
            away_goals = int(away_goals)
            if home_goals > away_goals:
                label = 'V'    
            else:
                label = 'P' if (home_goals < away_goals) else 'N'
        else:
            label = 'NAN'

        return label

    ### INIZIO ___________ FIX PREDIZIONI MANCANTI
    def read_all_predictions(self, cleaned):
        file = "temp/all_descriptive_prediction.csv" if cleaned != True else "files/cleaned_descriptive_predictions.csv"
        self.df = pd.read_csv(file, index_col=0)
    
    def recovery_games(self):
        """quello descritto nel metodo get_predictions non è l'unico problema, in quanto ci siano partite che sono state rimandate. Ovviamente i pronostici vengono fatti su due date diverse:
        - sulla data originale della partita (che poi viene rimandata)
        - sulla data rimandata
        Per questo devo cancellare le righe relative alle partite che non si sono più svolte in quella data e tenere solo i recuperi
        """
        recoveries = self.df.copy()
        for k, match in self.matches.iterrows():
            h_team, a_team = match.home, match.away
    
            recovery = recoveries[(recoveries['home']==h_team) & (recoveries['away']==a_team)]
            if len(recovery) > 1:
                recoveries.drop((recoveries[(recoveries['home']==h_team) & (recoveries['away']==a_team)])[:1].index, inplace=True)

        self.recoveries = recoveries
        """
        Devo fare il reset dell'index. Questo perché quando cerco di inserire un nuovo elemento nel dataframe, avendo eliminato in precedenza le partite "fasulle" (perché poi ci sono i recuperi) nel dataframe, quando gli passo l'indice questo non è relativo alla posizione, ma al vecchio indice e quindi se inserisco un valore con quel valore, potrebbe sovrascrivere quel record.
        Ad esempio, abbiamo sulla stagione 21/22 379 record. 
        C'è un record con indice 379, se io cercassi di fare df.at(379, ['example']) = 0, all'indice 379 (non alla posizione) viene settata a 0 la colonna 'example'.        
        """
        range_index = [i for i in range(len(self.recoveries))]
        self.recoveries['index'] = range_index 
        self.recoveries = self.recoveries.set_index('index') 

    def matches_not_found(self):
        """
        Ci potrebbero essere partite che non sono state trovate, quindi confronto i match che ci sono nel dataframe dei risultati e in quello scaricato da football predictions.
        C'è quindi un altro problema: i link potrebbero essere errati, quindi con lo scraping non vengono prelevati. 

        Bisogna cercare nel giorno della partita e cercare nella relativa pagina l'href che contiene la partita.
        """
        count = len(self.recoveries)
        
        for k, res in self.matches.iterrows():
            if len(self.recoveries[(self.recoveries['home']==res.home) & (self.recoveries['away']==res.away)]) < 1:
                
                print(res.date, res.home, res.away) #stampo quali sono i match che non sono stati trovati
                
                converted_data = pd.to_datetime(res.date, format='%Y-%m-%d', errors='coerce').date()
                new_date = converted_data.strftime('%d-%m-%Y')

                pageTree = requests.get('https://footballpredictions.com/footballpredictions/?date='+new_date)
                soup = BeautifulSoup(pageTree.text, features="lxml")
                links = soup.find_all('a', href=True)
                links = [link['href'] for link in links if (res.home.lower() in link['href']) or (res.away.lower() in link['href'])]
                cleaned_links = list(dict.fromkeys(links))
                if len(cleaned_links) > 0: 
                    home, away, text, label = self.get_prediction(cleaned_links[0])
                    
                    self.recoveries.at[count, 'date'] = res.date
                    self.recoveries.at[count, 'home'] = self.check_name(home)
                    self.recoveries.at[count, 'away'] = self.check_name(away)
                    
                    text = '\n\n'.join(text)
                    self.recoveries.at[count, 'description'] = text
                    self.recoveries.at[count, 'prediction'] = label

                    count += 1 #questo contatore serve per inserire in una determinata posizione
    
    def fix_dates(self):
        """Ho visto che alcune date non combaciano, in quanto su football predictions alcune date sono sballate (non combaciano al giorno stesso effettivo della partita, ma al giorno precedente) quindi per fare il match tra i due dataset (questo con le descrizioni delle predizioni e quello del match con la data corretta) devo considerare squadra home e away.
        """
        self.df = pd.merge(self.matches, self.recoveries[['home','away', 'description', 'prediction']], on=['home', 'away'])
        self.df['date'] = pd.to_datetime(self.df['date'], format='%Y-%m-%d')
        self.df.sort_values(by=['date'], inplace=True)

        self.df.to_csv('files/cleaned_descriptive_predictions.csv')
    ### FINE ___________ FIX PREDIZIONI MANCANTI
### FINE ___________ DOWNLOAD PREDIZIONI

    def read_cleaned_predictions(self):
        self.df = pd.read_csv('files/cleaned_descriptive_predictions.csv', index_col=0)
