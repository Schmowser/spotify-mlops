#!/usr/bin/python

import sys
from sklearn.model_selection import train_test_split
import pandas as pd


target_label = str(sys.argv[1])
print('Target Label:',  target_label)

X = pd.read_csv('./data/data.csv')
y = X[target_label]

X_train, X_unseen, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

print(X_train.shape)
print(X_unseen.shape)

X_train.to_csv('./data/training_data.csv', index=False)
X_unseen.to_csv('./data/unseen_data.csv', index=False)

X_train.to_csv('./mongo-seed/training_data.csv', index=False)
X_unseen.to_csv('./mongo-seed/unseen_data.csv', index=False)
