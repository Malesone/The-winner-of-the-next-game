path_stats = 'Serie A/'

###### CSV FILES ######
football_predictions = path_stats+'FootballPredictions/'
    ###### CSV da lavorare ######
championship = path_stats+'Championships/{}.csv' #file che contiene tutte le partite del campionato (giocate e non giocate, con il relativo risultato) -> una stagione
stats = path_stats+'Stats/'
statistics = stats+'{}.csv' #dataset contenente tutte le statistiche utili per ciascuna squadra in ciascun match (1 season)
merged_statistics = stats+'all_stats.csv' #dataset merge delle stagioni
matches_description = football_predictions+'matches.csv' #dataset con testo e predizione di FootballPrediction

dataset_without_text = stats+'cleaned_stats.csv' #dataset con le differenze (generato da analysis)
completed_dataset = path_stats+'completed_dataset.csv' #dataset completo, con statistiche, testo e predizione di FootballPrediction (generato da analysis)
    ###### CSV da lavorare ######

    ###### CSV completi ######
ranks = path_stats+'Ranks/'
ranking = ranks+'{}.csv' 

cleaned_matches_description = football_predictions+'cleaned_news.csv' 
championship_actual_season = championship.format('2022-2023')
    
    ###### CSV completi ######
next_matches = path_stats+'next_matches.csv'
final_dataset = path_stats+'{} final_dataset.csv' #dataset con i nomi delle squadre convertiti, con le statistiche e la predizione sul testo
    ###### CSV completi ######
###### CSV FILES ######

###### ML MODEL ######
path_ML = 'ML Model/'
## con TfidfVectorizer
TfidfVectorizer = path_ML+'Tfidf_vectorizer.pk'
classificatorTfIdf = path_ML+'Tfidf_text_DecisionTree.model'
final_classificator_Tfidf = path_ML+'Tfidf_final_model_RF.model' #classificatore con Tfidf
## con CountVectorizer
CountVectorizer = path_ML+'CV_vectorizer.pk'
classificatorCV = path_ML+'CV_text_DecisionTree.model'
classificatorCV_LR = path_ML+'CV_text_LogisticRegression.model'
final_classificator_CV = path_ML+'CV_final_model_RF.model' #classificatore con CV
###### ML MODEL ######

json_link_matches = football_predictions+'links.json' #file json con chiave il 
synonyms = path_stats+'synonyms.json' 
teams_codes = path_stats+'teams.json' #squadre con codici

