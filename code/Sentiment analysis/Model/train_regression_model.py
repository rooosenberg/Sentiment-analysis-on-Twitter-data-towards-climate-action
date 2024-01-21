
import joblib
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression

# load in train data for the labels
data_df_labels = pd.read_csv ('./small_training_set_pp.csv')
# load embedded train data
X = pd.read_csv ('../embedding_training_data.csv')

# pick out relevant data for training, this was done for the dataset before embedding aswell
data_df_labels = data_df_labels.dropna()

# replace the labels [0,4] with [0,1]
data_df_labels['labels'] = data_df_labels['labels'].replace(4,1)
labels = data_df_labels['labels']

# this model is the best according to gridsearch (se colab notebook), accuracy 0.7913 when tested
# now train on the whole training dataset
reg_model = LogisticRegression(solver="liblinear", penalty='l1')
reg_model.fit(X, labels)

import joblib
joblib.dump(reg_model, './reg_model_all_data.pkl')
