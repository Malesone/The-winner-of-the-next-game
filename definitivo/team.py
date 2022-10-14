class Team:
    def __init__(self, id, name, matches):
        self.id = id
        self.name = name
        self.matches = matches
    
    def get_avg_last_X_matches(self, X, date, avg_features):
        rows = self.matches[self.matches.date < date]
        if X < len(rows):
            rows = rows[-X:]
        averages = rows[avg_features].mean()
        return averages

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