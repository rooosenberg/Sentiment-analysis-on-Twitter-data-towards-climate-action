
import joblib
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression


#X_data = pd.read_csv('../embedding_BERT.csv')
X_data = pd.read_csv('../embedding_data_to_label.csv')

# load regression model
import joblib
reg_model = joblib.load('./reg_model_all_data.pkl')


# predict labels of data
labels = reg_model.predict(X_data)

#print(labels)


# save labels
pd.DataFrame(labels).to_csv("./data_test/labels_BERT_test.csv")
