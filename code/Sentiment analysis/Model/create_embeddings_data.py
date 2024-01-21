""" This file creates """

import pandas as pd
import numpy as np
import torch
from transformers import BertModel, BertTokenizer
from transformers import AutoModel, AutoTokenizer
from transformers import RobertaTokenizer, RobertaModel
from sklearn.linear_model import LogisticRegression


#df = pd.read_csv ('small_training_set_pp.csv')
df = pd.read_csv ('data_to_label_drive.csv')

# pick out relevant data for training
df = df.dropna()

device = 'cuda'

# create model
model = BertModel.from_pretrained("bert-base-uncased")
model = model.to(device)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# create embeddings
len = 512
def encode_text(text):

    input_ids = torch.tensor([tokenizer.encode(text, max_length=len, truncation=True)]).to(device)
    model_var = model(input_ids)[0].mean(1)[0].detach()
    return model_var.cpu().numpy()


X_data = np.array(list(df.Tweet.apply(encode_text).values))

#save embedding
pd.DataFrame(X_data).to_csv('../embedding_data_to_label.csv')
