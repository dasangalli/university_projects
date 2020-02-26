PROGETTO DI TEXT MINING AND SEARCH - README

1) E' sempre necessario eseguire il primo chunk per caricare le librerie necessarie

2) Se non si desidera eseguire tutto il codice, per comodità sono stati creati diversi dumps dei dataset (vedi materiale allegato), corrispondenti a diverse fasi/tasks
	
	2.1) è stato creato un dataset chiamato "df_amz_all.joblib", ottenuto dall'unione di tutti i datasets utilizzati 
	
	2.2) è stato creato un dataset chiamato "df_cluster" in cui alle reviews sono state applicate le operazioni di rimozione degli accenti, dei simboli, sono state rimosse le parole contratte e sostituite con la loro forma estesa e sono stati eliminati gli eventuali duplicati (utilizzare questo dump se si vuole solamente eseguire il codice relativo alla parte di clustering)
	
	2.3) è stato creato un dataset chiamato "df_category", da utilizzare per fare classificazione sulle categorie di prodotti. Questo è un dataset già pulito, a cui sono già state applicate le operazioni di preprocessing (operazioni descritti al punto 2.2 ed in più la lemmatizzazione)

	2.4) è stato creato un dataset chiamato "df_rating", da utilizzare per fare sentiment analysis. Anche questo dataset è già pulito, a cui sono già state applicate le operazioni di preprocessing (operazioni descritti al punto 2.2 ed in più la lemmatizzazione)


	    

