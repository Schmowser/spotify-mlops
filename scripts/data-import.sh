python ./scripts/seen_unseen_split.py
mongoimport --type csv -d songdb -c training_data --headerline --drop ./data/training_data.csv
mongoimport --type csv -d songdb -c unseen_data --headerline --drop ./data/unseen_data.csv