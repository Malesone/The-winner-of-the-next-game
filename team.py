import pandas as pd 

class Team:
    def __init__(self, id, name, matches):
        self.id = id
        self.name = name
        self.matches = matches
    
    def get_avg_last_X_matches(self, X, date, avg_features):
        change = False
        averages = None
        rows = self.matches[self.matches.date < date]

        if len(rows) > 0:
            change = True
            if X < len(rows):
                rows = rows[-X:]
            averages = rows[avg_features].mean()

        return averages, change

    def get_avg_all_matches(self, date, avg_features):
        #prende la media di tutti i match precedenti alla data del match preso in considerazione
        #il valore ritornato infatti è la riga di medie relative ai valori precedenti 
        change = False
        averages = None
        rows = self.matches[self.matches.date < date]
        if len(rows) > 1:
            averages = rows[avg_features].mean()
            change = True

        return averages, change

    def get_previous(self, team2, date):
        #metodo per ottenere il match precedente in cui le due squadre si sono scontrate
        res = self.matches[(self.matches.date < date) & (self.matches.team2 == team2)]
        if len(res) == 0 or res.result.values[0] == 'N' or res.result.values[0] == 'P':
            return False
        else:
            return True
        