# The winner of the next match
Football (aka soccer) is one of the most popular sports worldwide. There are plenty of press sources, newspaper articles, news, tweets etc. that discuss football on a daily basis and before matches.

The aim of the project is to define an automatic system to **predict the outcome of the matches** starting from the news concerning the teams involved in the match published in the days and weeks preceding the match. It is also possible to use other statistical data to make predictions regarding matches.

In particular, the project must:
- Choose a source of information from which to draw news for a football season in a league of your choice;
- Collect the actual results of the matches of the season in question;
- Collect other statistical information relating to players or teams
- Use news text analysis in conjunction with statistical sources to predict the outcome of specific matches. The only rule is that **the system can only use information whose date is prior to the match date**.

## References
* Radinsky, K., & Horvitz, E. (2013, February). Mining the web to predict future events. In Proceedings of the sixth ACM international conference on Web search and data mining (pp. 255-264). [link](https://dl.acm.org/doi/pdf/10.1145/2433396.2433431)
* Chen, W., Yeo, C. K., Lau, C. T., & Lee, B. S. (2018). Leveraging social media news to predict stock index movement using RNN-boost. Data & Knowledge Engineering, 118, 14-24. [link](https://www.sciencedirect.com/science/article/pii/S0169023X17305839)
* Peng, Y., & Jiang, H. (2015). Leverage financial news to predict stock price movements using word embeddings and deep neural networks. arXiv preprint arXiv:1506.07220. [link](https://arxiv.org/abs/1506.07220)


## Ordine esecuzione
Lanciare lo script `completati/download_dati.ipynb` per poter fare scraping dei dati e verranno creati: 
- il file `matches2.csv` in `SerieA/Season21_22` che contiene tutti i match giocati dalle squadre
- un file `name_team.csv` in `SerieA/Matches` contenente tutte le informazioni relative alle partite giocate da ogni singola squadre

Trovate queste informazioni deve essere lanciato lo script che permette di calcolare le features, ovvero le medie delle statistiche di ogni partita. Questo script si trova in `completati/features.ipynb` che genere tanti csv quante le squadre dove per ciascuna partita ricalcola i dati facendo la media con i match precedenti `SerieA/Season21_22/AvgStats`.

Per poter aiutarci con la predizione un altro dato utile è il rank che permette di calcolare quanto sia forte la squadra in base a tot. stagioni passate. 
Il rank viene calcolato in `completati/ranks.ipynb` e genera il file `SerieA/Season21_22/rank.csv`.

## Organizzazione repo
Per poter effettuare il download del dataset con tutti match di una stagione, bisogna lanciare lo script "download_dati.py". 
Di default è impostato il download dei dati della Serie A per la stagione 2021/2022.
Uno sviluppo futuro è la possibilità da parte dell'utente di scegliere il campionato da cui si vogliono estrarre i dati.

Una volta che i dati vengono scaricati, vengono salvati in una cartella il cui path è Lega/Stagione ad esempio "Serie A/Season21_22/dataset.csv".
Il dataset è organizzato secondo le squadre che giocano in casa.
Nel dataset ci sono i seguenti dati: 

### Normalizzazione dati
I dati devono essere normalizzati, perché alcuni modelli di ML non possono accettare stringhe. Per questo vengono normalizzati i dati.
L'etichetta con la quale si vuole classificare è "result" che ha i valori V/P/N. 
Questi valori vengono associati a dei numeri V = 1, P = 2, N = 0. 
I nomi delle squadre vengono associati anch'essi a dei numeri e quindi viene effettuata l'operazione di dummy.
In questo modo vengono cancellate dal dataset le colonne "h_team" e "a_team" e vengono sostituite da tot colonne (quanto il numero di squadre) * 2, perché con il dummy avranno valore 1 solo le squadre che in quel match si scontrano. 
Ad esempio in Serie A sono 20*2 colonne aggiuntive perché ci sono 20 squadre home e 20 squadre away.

Lo script da lanciare è "dummy.py".

### Classificazione
Il modello utilizzato per la previsione dei risultati è supervisionato, in quanto si debba allenare il modello attraverso dati (train set) di cui si conoscono le classi (0,1,2) e poi viene fatta la previsione su un test set. 

Per questo bisogna lanciare lo script "classification.py". 

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

# Creazione folder
Per popolare la cartella dobbiamo scaricare tutte le stagioni precedenti. Si esegue "download_and_merge_matches.ipynb".

Successivamente vengono scaricate tutte le partite con le statistiche per ciascuna squadra e vengono creati tanti csv quante le stagioni considerate. 

Eseguendo "ranking.ipynb" è possibile scaricare i risultati di altre stagioni per poter calcolare il ranking delle squadre che si affrontano. 

Eseguendo "analysis.ipynb" vengono combinate tutte le partite creando un unico dataset e per ciascuna partita vengono calcolate le differenze come media delle 5 partite precedenti. 
Viene anche calcolato il rank delle due squadre (rank che si basa sugli scontri diretti delle due squadre)

Fatto ciò devo effettuare il merge tra questo dataset con il dataset contenente le statistiche. Viene fatto attraverso 

# Merge del testo con le statistiche
"completed_dataset.ipynb" ha il compito di riconciliare i dati (statstiche) delle partite con il testo di predizione.

# Creazione modello per l'analisi del testo
Il modello viene allenato attraverso "text analysis.ipynb" che permette prima di tokenizzare il testo, fare il fit transform del TfIdfVectorizer per poi predire il risultato

# Modello finale
Creato il modello di predizione del testo, bisogna fare il modello su tutti i dati attraverso "final_model.ipynb"

# Valutazione
Infine vengono prese le partite della prossima giornata, vengono calcolate le differenze delle medie, ottengo le predizioni sul testo ed infine predico il risultato finale