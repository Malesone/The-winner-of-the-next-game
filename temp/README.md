# Download statistiche
Per poter scaricare tutti i match di una stagione devo eseguire lo script download.py. 
Questo viene fatto tramite download.ipynb.
Il file che viene salvato con i vari match si chiama "matches_ordered_by_date.csv" e contiene i seguenti dati:
- team1 
- date 
- matchday 
- stadium 
- result
- goals 
- team2 
- total_shots 
- shots_on_target 
- goals_on_penalty 
- total_penalties
- completed_passings 
- total_passings
- corners 
- percentage_possession
- fouls
- yellow_cards 
- red_cards
Tutti questi dati sono relativi a team1, indipendentemente dal fatto che giochi in casa o in trasferta.

# Download informazioni pre-match
Per poter scaricare le informazioni pre-match di qualsiasi partita, bisogna eseguire lo script text_analysos che consente di scaricaree dal sito https://footballpredictions.com/ le predizioni effettuate. 
Per poter effettuare questa operazione devo utilizzare text_analysis.ipynb che permette al termine di scaricare un csv "all_descriptive_predictions.csv" con le predizioni per ciascuna partita.

Il problema è che ci sono anche le predizioni doppie, perché su alcune partite sono stati effettuati dei recuperi, per questo bisogna elaborare ancora i dati fino ad ottenere un file "cleaned_descriptive_predictions.csv".

Vengono salvate anche quelle partite su cui non è stata trovata alcuna predizione, quindi ho due soluzioni: 
- inserire un valore nullo quando si fa la classificazione
- fare la classificazione lo stesso
- eliminare le righe nulle (predizione non presenze

## Analisi dei match
Avendo eliminato i match in cui non ci sono predizioni, dovrei eliminare gli stessi match nelle statistiche, altrimenti il modello si sballa.
Prima di fare questo, vado a combinare i dati con le varie statistiche. 
Questo è fatto tramite lo script analysis.py eseguito con analysis.ipynb.
Ottengo un file "diff_matches.csv" che va a combinare le statistiche della squadra di casa e trasferta.
Da qui poi vado a cancellare i relativi record per cui non ho trovato le predizioni.

# Integrazione dataset
Le statistiche sono già composte, devo integrare le etichette di predizione che vengono ottenute dall'analisi del testo.

