# Creazione folder
Per popolare la cartella dobbiamo scaricare tutte le stagioni precedenti. Si esegue "download and merge mathes.ipynb".

Successivamente vengono scaricate tutte le partite con le statistiche per ciascuna squadra e vengono creati tanti csv quante le stagioni considerate. 

Eseguendo "ranking.ipynb" è possibile scaricare i risultati di altre stagioni per poter calcolare il ranking delle squadre che si affrontano. 

Eseguendo "analysis.ipynb" vengono combinate tutte le partite creando un unico dataset e per ciascuna partita vengono calcolate le differenze come media delle 5 partite precedenti. 
Viene anche calcolato il rank delle due squadre (rank che si basa sugli scontri diretti delle due squadre)

<<<<<<< HEAD
# Download del testo
Attraverso "football_predictions.ipynb" vengono scaricate le predizioni. 
Il file che si ottiene eseguendo tutto il processo è "cleaned_descriptions.csv".
=======
## Exam rules
Exam dates are just for the registration of the final grade. The project discussion will be set by appointment.

PROCEDURE

Subscribe to any available date
Contact Prof. Ferrara as soon as
The project is finished and ready to be discussed
After the date of your subscription
Setup an appointment and discuss your work


If you are interested in doing your final master thesis on these topics, the final project may be a preliminary work in view of the thesis. In this case, discuss the contents with Prof. Ferrara.

The final project consists in the preparation of a short study on one of the topics of the course, identifying a precise research question and measurable objectives. The project will propose a methodology for solving the research question and provide an experimental verification of the results obtained according to results evaluation metrics. The emphasis is not on obtaining high performance but rather on the critical discussion of the results obtained in order to understand the potential effectiveness of the proposed methodology.

The results must be documented in a short article of not less than 4 pages and no more than 8, composed according to the guidelines provided by the lecturers. Students have also to provide access to a GitHub repository containing the code and reproducible experimental results. Finally, the project will be discussed by presenting a 10 minute presentation with slides.

>>>>>>> 90e218156a1523485c65dca8b6e2d6bf38e5fca2

Fatto ciò devo effettuare il merge tra questo dataset con il dataset contenente le statistiche. Viene fatto attraverso 

# Merge del testo con le statistiche
"completed_dataset.ipynb" ha il compito di riconciliare i dati (statstiche) delle partite con il testo di predizione.

# Creazione modello per l'analisi del testo
Il modello viene allenato attraverso "text analysis.ipynb" che permette prima di tokenizzare il testo, fare il fit transform del TfIdfVectorizer per poi predire il risultato

# Modello finale
Creato il modello di predizione del testo, bisogna fare il modello su tutti i dati attraverso "final_model.ipynb"

# Valutazione
Infine vengono prese le partite della prossima giornata, vengono calcolate le differenze delle medie, ottengo le predizioni sul testo ed infine predico il risultato finale