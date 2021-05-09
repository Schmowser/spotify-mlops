import pandas as pd
import matplotlib.pyplot as plt
from data_drift_detector import DataDriftDetector

training_df = pd.read_csv('./../data/training_data.csv')
unseen_df = pd.read_csv('./../data/unseen_data.csv')

# initialize detector
detector = DataDriftDetector(df_prior=training_df, df_post=unseen_df)

# calculate jensen shannon distance between each column of the 2 data sets
print(detector.calculate_drift())

#detector.plot_numeric_to_numeric()

training_hist_plot = training_df.hist(column='danceability')
unseen_hist_plot = unseen_df.hist(column='danceability')

plt.show()
