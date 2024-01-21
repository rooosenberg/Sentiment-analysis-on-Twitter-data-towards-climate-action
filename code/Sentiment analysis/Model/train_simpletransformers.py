
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import joblib
import pickle
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
fixed_random_state = 5

# load in train data for the labels
data_df_labels = pd.read_csv ('./small_training_set_pp.csv')
# load embedded train data
X = pd.read_csv ('../embedding_training_data.csv')

# pick out relevant data for training, this was done for the dataset before embedding aswell
data_df_labels = data_df_labels.dropna()

# replace the labels [0,4] with [0,1]
data_df_labels['labels'] = data_df_labels['labels'].replace(4,1)
labels = data_df_labels['labels']

df_train = pd.concat([X, labels])

# create train dataset
train_df, test_df = train_test_split(df_train, test_size=0.2, random_state=fixed_random_state)

train_args = {
    'sliding_window': True,
    'max_seq_length': 64,
    'num_train_epochs': 2,
    'train_batch_size': 128,
    'fp16': True,
    'output_dir': '/outputs/',
}

# logging
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

device = 'cuda'

# model
model_args = ClassificationArgs(num_train_epochs=1)
model = ClassificationModel('bertweet','vinai/bertweet-base', num_labels = 2,
    args=model_args)

model = model.to(device)

model.train_model(train_df)
result, model_outputs, wrong_predictions = model.eval_model(eval_df)

print('result')
print(result)
print('model_outputs')

import joblib
joblib.dump(model, './simple_model.pkl')
