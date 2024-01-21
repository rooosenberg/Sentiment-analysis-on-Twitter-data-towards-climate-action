# Sentiment analysis on Twitter data towards climate action

## Introduction 
The code in this repository features sentiment analysis with VADER, TextBlob and tranfer learning wth BERT + trained regression model. The sentiment is positive, negative and neutral. The BERT-based model is binary,positive/negative. 
For more details regarding methods, result and models see the paper ["Sentiment analysis on Twitter data towards climate action", Emelie Rosenberg, Carlota Tarazona, Fermín Mallor, Hamidreza Eivazi, David Pastor-Escuredo, Francesco Fuso-Nerini, Ricardo Vinuesa](https://doi.org/10.1016/j.rineng.2023.101287)

This site was built using [GitHub Pages](https://pages.github.com/).

## Data
- Training: The training of the Regression model was done with the Kaggle dataset [Sentiment140](https://www.kaggle.com/datasets/kazanova/sentiment140).
- Collected data: It was collected with the python package, Tweepy. 
- Annotated data: 247 tweets was annoteded as positive, neutral and negative.  

## BERT-model
The TweetBert model was used for tokanization. For more information about the model see [Hugging Face model card](https://huggingface.co/docs/transformers/model_doc/bertweet). 

## Regression model
The model can be found under code/Sentiment analysis/Model/



