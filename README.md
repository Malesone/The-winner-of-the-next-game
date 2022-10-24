# Creazione folder
Per popolare la cartella dobbiamo scaricare tutte le stagioni precedenti. Si esegue "download and merge mathes.ipynb".

Successivamente vengono scaricate tutte le partite con le statistiche per ciascuna squadra e vengono creati tanti csv quante le stagioni considerate. 

Eseguendo "ranking.ipynb" è possibile scaricare i risultati di altre stagioni per poter calcolare il ranking delle squadre che si affrontano. 

Eseguendo "analysis.ipynb" vengono combinate tutte le partite creando un unico dataset e per ciascuna partita vengono calcolate le differenze come media delle 5 partite precedenti. 
Viene anche calcolato il rank delle due squadre (rank che si basa sugli scontri diretti delle due squadre)

# Download del testo
Attraverso "football_predictions.ipynb" vengono scaricate le predizioni. 
Il file che si ottiene eseguendo tutto il processo è "cleaned_descriptions.csv".

Fatto ciò devo effettuare il merge tra questo dataset con il dataset contenente le statistiche. Viene fatto attraverso 

# Merge del testo con le statistiche
"completed_dataset.ipynb" ha il compito di riconciliare i dati (statstiche) delle partite con il testo di predizione.
