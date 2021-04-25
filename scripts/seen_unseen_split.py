from sklearn.model_selection import train_test_split
import pandas as pd


X = pd.read_csv('./data/data.csv')
y = X['popularity']

X_train, X_unseen, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

print(X_train.shape)
print(X_unseen.shape)

X_train.to_csv('./data/training_data.csv', index=False)
X_unseen.to_csv('./data/unseen_data.csv', index=False)
