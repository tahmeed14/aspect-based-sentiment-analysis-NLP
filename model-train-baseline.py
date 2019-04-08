# Aspect-Based Sentiment Analysis: Findings from Unstructured Natural Language
# Tahmeed Tureen - University of Michigan, Ann Arbor

# model-train-baseline.py
# Code to train the proposed baseline ASBA model

import pandas as pd
import math
from collections import Counter
from collections import defaultdict

# Read in the dataset that is row-wise based on aspect terms instead of review
aspect_terms_pd = pd.read_csv("aspect-terms-data.csv", index_col = False)

# We will have to re-format the dataset
aspect_terms_pd = aspect_terms_pd[['Review', 'Review ID', 'Aspect Term', 'Aspect Polarity']]

# For 3/24/2019, we are implementating the most basic baseline method proposed in the project update

# Split the data as 80% train and 20% dev (project update test)
train_index = math.floor(0.80 * aspect_terms_pd.shape[0]) # 80 % of the current data as training data

train_data = aspect_terms_pd.iloc[0:train_index, :]
test_data = aspect_terms_pd.iloc[train_index:aspect_terms_pd.shape[0], :]

print(aspect_terms_pd.shape)
print(train_data.shape)
print(test_data.shape)
print(train_data.shape[0] + test_data.shape[0])

# SubTask 1: Aspect Term Extraction
terms_bank = set(train_data['Aspect Term'])
print(len(terms_bank))



# SubTask 2: Sentiment Polarity Classifier


