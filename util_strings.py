path_stats = 'files/Serie A/'

championship = path_stats+'{} championship.csv' #file che contiene tutte le partite del campionato (giocate e non giocate, con il relativo risultato) -> una stagione
statistics = path_stats+'{} statistics.csv' #file che contiene tutte le statistiche utili per ciascuna squadra in ciascun match -> una stagione

merged_statistics = path_stats+'all stats.csv' #file che contiene tutte le statistiche utili per ciascuna squadra in ciascun match -> tutte le stagioni

matches_merged = path_stats+'matchesMerged/matches.csv' #unisce i match del punto precedente

dataset_without_text = path_stats+'dataset_without_text.csv'
completed_dataset = path_stats+'completed_dataset.csv'

ranking = path_stats+'{}.csv'

json_link_matches = path_stats+'fp_links.json'

matches_description = path_stats+'matches_description.csv'
cleaned_matches_description = path_stats+'cleaned_descriptions.csv'

synonyms = path_stats+'synonyms.json'

###### BEGIN:   ML MODEL ######
path_ML = 'ML Model/'
text_analysis = path_ML+'decision tree text analysis.model'

###### END:     ML MODEL ######

championship_actual_season = path_stats+'2022-2023 championship.csv'

next_matches = path_stats+'next_matches.csv'

vectorizer = path_ML+'vectorizer.pk'