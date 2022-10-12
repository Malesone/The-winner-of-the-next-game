import pandas as pd
import numpy as np 
from tqdm import tqdm

class MatchAnalysis:
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
    
    def __init__(self):
        self.read_matches()
        #self.convert_stadium()

    def read_matches(self):
        self.matches_fe_team = pd.read_csv("matches_fe_team.csv", index_col=0)
        self.matches_fe_team.reset_index(drop=True, inplace=True)

    def convert_stadium(self):
        #dato che il campo stadium come valori può avere "Casa" o "Ospiti" devo convertire questi valori in "0" e "1"
        self.matches_fe_team.stadium = self.matches_fe_team.stadium.replace(['Casa'], 0)
        self.matches_fe_team.stadium = self.matches_fe_team.stadium.replace(['Ospiti'], 1)

    def create_team_dataset(self):
        #per ogni squadra nel campionato viene creato un dataset che contiene tutte le partite giocate dalla squadra con le relative statistiche
        self.matches_by_team = []
        for team in sorted(self.matches_fe_team.team.unique()):
            self.matches_by_team.append(self.matches_fe_team[self.matches_fe_team.team == team])

    def calculate_avg(self):
        stats_of_all_teams = {}

    def divide_and_merge_home_away(self):
        #dato che il dataset scaricato contiene le informazioni relative alle statistiche delle squadre, ci saranno per ogni partita 2 record che si riferiscono alla stessa partita: un record per la squadra di casa e uno per la squadra di trasferta. Divido quindi chi gioca in casa da chi gioca in trasferta andando a considerare il campo "Stadio" che dice appunto se la squadra gioca in casa o in trasferta (la squadra presa di riferimento è quella su cui vengono prese le statistiche). Successivamente i 2 record che si riferiscono alla stessa partita (uno nel dataset home_games, uno nel dataset away_games) vengono combinati ed alla fine ottengo un dataset 
        home_games = self.matches_fe_team[self.matches_fe_team['Stadio']=='Casa']
        away_games = self.matches_fe_team[self.matches_fe_team['Stadio']=='Ospiti']
        
        home_games = home_games.rename(columns=self.rename_fields)
        away_games = away_games.rename(columns=self.rename_fields)

        column_needed = np.array(self.rename_fields.values())
        home_games = home_games[column_needed]
        away_games = away_games[column_needed]

        self.getDiff_home_away(home_games, away_games)

    def getDiff_home_away(self, hm, am):
        self.diff_dataset = []
        for index, home_match in hm.iterrows():
            away_match = am[(am['date'] == home_match['date']) & (am['team2'] == home_match['team1']) & (am['team1'] == home_match['team2'])]
            away_match_reduced = away_match.drop(columns = ['date', 'team1', 'team2', 'stadium', 'matchday', 'result'])
            for col in away_match_reduced.columns:
                home_match[col] = home_match[col] - away_match_reduced[col].values[0]
            self.diff_dataset.append(home_match)

        self.diff_dataset = pd.DataFrame(self.diff_dataset)
        self.diff_dataset['date'] = pd.to_datetime(self.diff_dataset ['date'], format='%d-%m-%Y') #devo convertire la data altrimenti mi dà problemi quando la lego         

        self.diff_dataset.drop(columns=['stadium', 'matchday'], inplace=True)
        self.diff_dataset.sort_values(by=["date"], inplace=True)
        self.diff_dataset.reset_index(drop=True, inplace=True)

        self.diff_dataset.rename(columns={'team1':'home', 'team2': 'away'}, inplace=True)
        self.diff_dataset.to_csv("diff_matches.csv")

    def readDiff_home_away(self):
        self.diff_dataset = pd.read_csv("diff_matches.csv", index_col=0)


    def get_dummies(self):
        stacked = self.diff_dataset[['home', 'away']].stack()
        index = stacked.index.get_level_values(0)
        result = pd.crosstab(index=index, columns=stacked)
        result.index.name = None
        result.columns.name = None

        dummy_match = pd.get_dummies(self.diff_dataset
                ,columns = ['home']
                ,prefix = ['h']
                )

        dummy_match = dummy_match.drop(['away'], axis=1)
        pos = 0
        for col in result.columns:
            dummy_match.insert(pos, col, result[col])
            pos += 1

        self.diff_dataset = dummy_match
        