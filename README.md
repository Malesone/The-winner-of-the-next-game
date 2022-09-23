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


## Organizzazione repo
Per poter effettuare il download del dataset con tutti match di una stagione, bisogna lanciare lo script "download_dati.py". 
Di default è impostato il download dei dati della Serie A per la stagione 2021/2022.
Uno sviluppo futuro è la possibilità da parte dell'utente di scegliere il campionato da cui si vogliono estrarre i dati.

Una volta che i dati vengono scaricati, vengono salvati in una cartella il cui path è Lega/Stagione ad esempio "Serie A/Season21_22/dataset.csv".
Il dataset è organizzato secondo le squadre che giocano in casa.
Nel dataset ci sono i seguenti dati: 

Campo | Descrizione
--- | ---
`h_team` | Squadra di casa
`result` | Risultato finale della partita (V=vittoria, P=sconfitta, N=pareggio)
`h_goals` | Goal effettuati dalla squadra di casa
`a_team` | Squadra ospite
`a_goals` | Goal effettuati dalla squadra ospite
`h_total_shots` | Tiri totali casa
`h_shots_on_target` | Tiri nello specchio casa
`h_goals_on_penalty` | Goal su rigore casa
`h_total_penalties` | Rigori totali casa
`h_corners` | Corner casa
`h_completed_passings` | Passaggi completati casa
`h_total_passings` | Passaggi totali casa
`h_fouls` | Falli effettuati casa
`h_yellow_cards` | Cartellini gialli casa
`h_red_cards` | Cartellini rossi casa
`h_percentage_possession` | Percentuale possesso casa
`a_total_shots` | Tiri totali ospiti
`a_shots_on_target` | Tiri nello specchio ospiti
`a_goals_on_penalty` | Goal su rigore ospiti
`a_total_penalties` | Rigori totali ospiti
`a_corners` | Corner ospiti
`a_completed_passings` | Passaggi completati ospiti
`a_total_passings` | Passaggi totali ospiti
`a_yellow_cards` | Cartellini gialli ospiti
`a_red_cards` | Cartellini rossi ospiti
`a_fouls` | Falli effettuati ospiti
`a_percentage_possession` | Percentuale possesso ospiti

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
