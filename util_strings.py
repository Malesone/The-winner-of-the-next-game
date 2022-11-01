path_stats = 'Serie A/'

###### CSV FILES ######
football_predictions = path_stats+'FootballPredictions/'
    ###### CSV da lavorare ######
championship = path_stats+'Championships/{}.csv' #file che contiene tutte le partite del campionato (giocate e non giocate, con il relativo risultato) -> una stagione
stats = path_stats+'Stats/'
statistics = stats+'{}.csv' #dataset contenente tutte le statistiche utili per ciascuna squadra in ciascun match (1 season)
merged_statistics = path_stats+'all_stats.csv' #dataset contenente le statistiche per ciascuna squadra in ciascun match giocato (tutte le stagioni)
matches_description = football_predictions+'matches.csv' #dataset con testo e predizione di FootballPrediction

dataset_without_text = path_stats+'cleaned_stats.csv' #dataset definitivo per le statistiche
completed_dataset = path_stats+'completed_dataset.csv' #dataset completo, con statistiche, testo e predizione di FootballPrediction
    ###### CSV da lavorare ######

    ###### CSV completi ######
ranks = path_stats+'Ranks/'
ranking = ranks+'{}.csv' 

cleaned_matches_description = football_predictions+'cleaned_descriptions.csv'
championship_actual_season = championship.format('2022-2023')
    
    ###### CSV completi ######
next_matches = path_stats+'next_matches.csv'
final_dataset = path_stats+'final_dataset.csv' #dataset con i nomi delle squadre convertiti, con le statistiche e la predizione sul testo
    ###### CSV completi ######
###### CSV FILES ######

###### ML MODEL ######
path_ML = 'ML Model/'
vectorizer = path_ML+'vectorizer.pk'
text_analysis = path_ML+'DT text analysis.model'
classificator_FP = path_ML+'DT text analysis.model'
classificator = path_ML+'RF final model.model'
###### ML MODEL ######

json_link_matches = football_predictions+'links.json' #file json con chiave il 
synonyms = path_stats+'synonyms.json' 
teams_codes = path_stats+'teams.json' #squadre con codici

