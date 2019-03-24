# Aspect-Based Sentiment Analysis: Findings from Unstructured Natural Language
# Tahmeed Tureen - University of Michigan, Ann Arbor

# model-train-baseline.py
# Code to train the proposed baseline ASBA model

import pandas as pd

# Read in Data
reviews_pd = pd.read_csv("processed-reviews.csv", index_col = False)

# We are currently only interested in aspect-term extraction and aspect-term sentiment classification
# Column Names for convenience
# ['Aspect Term', 'Aspect Polarity', 'Category', 'Category Polarity', 'Review', 'Review ID']

# We will have to re-format the dataset
aspects_pd = reviews_pd[['Review', 'Review ID', 'Aspect Term', 'Aspect Polarity', 'Aspect Count']]

print(list(aspects_pd))

print("Total number of reviews: ", aspects_pd.shape[0])
print("Total number of aspect terms in training data: ", sum(aspects_pd['Aspect Count']))

list_aspects_data = []
# Since reviews can have multiple aspect terms we need to re-format the data set so that each row represents the aspect
for row in aspects_pd.itertuples(index = True, name = "Pandas"):
	
	terms_list, polarity_list = row[3], row[4]

	print(type(terms_list))
	print(type(polarity_list))

	print(terms_list)
	print(polarity_list)

	print(len(terms_list))
	print(len(polarity_list))
	print(len(terms_list) == len(polarity_list))
	
	# for term_index in range(len(terms_list)):

	# 	term_data = {}

	# 	term_data["Aspect Term"] = terms_list[term_index]
	# 	term_data["Aspect Polarity"] = polarity_list[term_index]
	# 	term_data["Review"] = row[1]
	# 	term_data["Review ID"] = row[2]

	# 	list_aspects_data.append(term_data)

print(len(list_aspects_data))




