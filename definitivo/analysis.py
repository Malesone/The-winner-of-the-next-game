from os import rename
import pandas as pd
class MatchAnalysis:
    def __init__(self, renamed_fields):
        self.renamed_fields = renamed_fields
        self.read_matches()
        self.convert_stadium()

    def read_matches(self):
        self.matches_fe_team = pd.read_csv("matches_fe_team.csv", index_col=0)
        self.matches_fe_team.reset_index(drop=True, inplace=True)
        self.matches_fe_team.drop(columns=['Avversario', 'Rs', 'Risultato', 'Girone'], inplace=True)

        self.renamed_fields['Data'] = 'date'
        self.renamed_fields['Stadio'] = 'stadium'
        self.matches_fe_team.rename(columns=self.renamed_fields, inplace=True)

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
        
        team_stats = team_stats.rename(columns=rename_fields) #rinomino le colonne per avere una nomenclatura 
        #team_stats = team_stats.drop(columns=['Stadio', 'Avversario', 'Rs', 'team', 'date', 'matchday', 'Risultato'])
        team_stats = team_stats.drop(columns=['Stadio', 'Avversario', 'Rs'])
        dataset = team_stats.drop(columns=['team', 'date', 'matchday', 'Risultato'])

        for single_col in dataset.columns:
            team_stats[single_col] = team_stats[single_col].astype(float) #converto la colonna in float se no vengono approssimati i valori per difetto
            team_column = dataset[single_col]
            
            for index, value in enumerate(team_column.values):
                sum = value if index == 0 else 0
                for from_0_to_index in range(index): 
                    sum += dataset.iloc[from_0_to_index][single_col]
                
                mean = (sum / index) if index > 0 else sum
                team_stats.at[index, single_col] = mean
        
        team_stats['date'] = pd.to_datetime(team_stats['date'], format='%d-%m-%Y') #devo convertire la data altrimenti mi dà problemi quando la lego 
        team_stats.to_csv("SerieA/Season21_22/AvgStats/"+file)