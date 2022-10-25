path_stats = 'files/Serie A/'

###### CSV FILES ######
    ###### CSV da lavorare ######
championship = path_stats+'{} championship.csv' #file che contiene tutte le partite del campionato (giocate e non giocate, con il relativo risultato) -> una stagione
statistics = path_stats+'{} statistics.csv' #dataset contenente tutte le statistiche utili per ciascuna squadra in ciascun match (1 season)
merged_statistics = path_stats+'all stats.csv' #dataset contenente le statistiche per ciascuna squadra in ciascun match giocato (tutte le stagioni)
matches_merged = path_stats+'matchesMerged/matches.csv' #unisce i match del punto precedente
matches_description = path_stats+'matches_description.csv' #dataset con testo e predizione di FootballPrediction

dataset_without_text = path_stats+'dataset_without_text.csv' #dataset definitivo per le statistiche
completed_dataset = path_stats+'completed_dataset.csv' #dataset completo, con statistiche, testo e predizione di FootballPrediction
    ###### CSV da lavorare ######

    ###### CSV completi ######
ranking = path_stats+'{}.csv' 

cleaned_matches_description = path_stats+'cleaned_descriptions.csv'
championship_actual_season = path_stats+'2022-2023 championship.csv'
    
    ###### CSV completi ######
next_matches = path_stats+'next_matches.csv'
final_dataset = path_stats+'final_dataset.csv' #dataset con i nomi delle squadre convertiti, con le statistiche e la predizione sul testo
    ###### CSV completi ######
###### CSV FILES ######

###### ML MODEL ######
path_ML = 'ML Model/'
vectorizer = path_ML+'vectorizer.pk'
text_analysis = path_ML+'decision tree text analysis.model'
classificator_FP = path_ML+'ta decision tree 0.942 (no syn).model'
classificator = path_ML+'random forest 0.549.model'
###### ML MODEL ######

json_link_matches = path_stats+'fp_links.json' #file json con chiave il 
synonyms = path_stats+'synonyms.json' #non più utilizzato

