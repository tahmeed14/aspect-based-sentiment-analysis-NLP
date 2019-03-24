# Aspect-Based Sentiment Analysis: Findings from Unstructured Natural Language
# Tahmeed Tureen - University of Michigan, Ann Arbor

# data-engin-tureen.py
# Code to process the XML format dataset from 2014 SemEval Task 4

import xml.etree.ElementTree as ET # Import XML parser library
import pandas as pd # import Pandas library
import numpy as np
import math
from collections import Counter
from collections import defaultdict

# I Data Processing of raw data
# Read in XML data
tree = ET.parse('../SemEval_14_Train/Restaurants_Train_v2.xml')
# tree = ET.parse('../SemEval_14_Train/play.xml')
root = tree.getroot()

# The data is nested like a tree because it's in XML format

# We will loop through all of the sentences (reviews)
# The whole XML data is nested under the root term: sentences
# This root has branches named "sentence" (individual review) and we have multiple of these

processed_reviews = [] # this list will contain dictionaries, eventually we will convert it to a Pandas DataFrame

for sen in root.findall("sentence"):
	# this dictionary will store the columns we are interested in storing for our processed dataset
	data_dict = {} 

	review = sen[0].text # assign the text review to this variable

	if sen.find("aspectTerms"): # if there exists aspect terms in review 

		# we make define these lists because a review can have multiple aspects
		term_tokens = [] # slot 1 for value_container
		term_pols = [] # slot 2 for value_container
		
		# Iterate through individual aspect terms and strip its polarity
		for branch in sen.find("aspectTerms").findall("aspectTerm"):
			term = branch.get("term")
			term_polarity = branch.get("polarity")

			term_tokens.append(term)
			term_pols.append(term_polarity)

	if sen.find("aspectCategories"): # if there exists labeled categories 

		# We define these lists because a review can have multiple aspects
		cat_tokens = [] # list of all of the labeled categories for the data
		cat_pols = [] # list of the associated polarities

		for branch in sen.find("aspectCategories").findall("aspectCategory"):
			category = branch.get("category")
			cat_polarity = branch.get("polarity")

			cat_tokens.append(category)
			cat_pols.append(cat_polarity)

	# Start assigning the values we just mined to appropriate keys in data_dict
	data_dict["Review ID"] = sen.attrib["id"]
	data_dict["Review"] = review
	data_dict["Aspect Term"] = term_tokens
	data_dict["Aspect Polarity"] = term_pols
	data_dict["Aspect Count"] = len(term_tokens)
	data_dict["Category"] = cat_tokens
	data_dict["Category Polarity"] = cat_pols
	data_dict["Category Count"] = len(cat_tokens)

	# each element in the following list will be a row for our processed dataset
	processed_reviews.append(data_dict) # append data_dict

# convert dataset to Pandas DF
reviews_pd = pd.DataFrame(processed_reviews)
# print(reviews_data_pd)

# Save as a CSV for further use
# path_csv = r"C:\\Users\\Tahmeed\\Dropbox\\Masters\\win-2019\\NLP_SI630\\final-project\\asba\\processed-reviews.csv"
# reviews_pd.to_csv(path_csv, index = None, header = True)


# II Data Processing to re-format datasets
aspects_terms_pd = reviews_pd[['Review', 'Review ID', 'Aspect Term', 'Aspect Polarity', 'Aspect Count']]

aspects_data_list = []

for row in aspects_terms_pd.itertuples():

	terms_list = row[3]
	pols_list = row[4]

	# print(len(terms_list) == len(pols_list))

	for i in range(len(terms_list)):
		data_dict = {}

		data_dict["Review ID"] = row[2]
		data_dict["Review"] = row[1]

		pol = pols_list[i]

		if pol == "conflict":
			pol = "neutral"

		data_dict["Aspect Term"] = terms_list[i]
		data_dict["Aspect Polarity"] = pol
		data_dict["All Aspect Terms"] = terms_list

		aspects_data_list.append(data_dict)

# Convert to Pandas Data Frame for convenience
aspect_terms_pd = pd.DataFrame(aspects_data_list)
aspect_terms_pd = aspect_terms_pd[['Review', 'Review ID', 'Aspect Term', 'Aspect Polarity', 'All Aspect Terms']] # re-order

# Save to a CSV for future use
path_csv = r"C:\\Users\\Tahmeed\\Dropbox\\Masters\\win-2019\\NLP_SI630\\final-project\\asba\\aspect-terms-data.csv"
aspect_terms_pd.to_csv(path_csv, index = None, header = True)


# Evaluation Metrics for Project Update (We will change this for the final project)
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
terms_bank = set(train_data['Aspect Term']) # extraction model
print(len(terms_bank))
print()

extract_preds = []

for row in test_data.itertuples():

	# tokenize the review
	rev_tokens = row[1].split()
	# print(rev_tokens)
	asp_terms = []

	for tok in rev_tokens:
		if tok in terms_bank:
			asp_terms.append(tok)

	data_dict = {}
	data_dict["Review ID"] = row[2]
	data_dict["Extracted Aspect Terms"] = asp_terms
	data_dict["True Aspect Terms"] = row[5]
	extract_preds.append(data_dict)

extract_preds_pd = pd.DataFrame(extract_preds)
# Save to a CSV for inspection
path_csv = r"C:\\Users\\Tahmeed\\Dropbox\\Masters\\win-2019\\NLP_SI630\\final-project\\asba\\extract-terms-data.csv"
extract_preds_pd.to_csv(path_csv, index = None, header = True)

pred_aspect_terms = np.array(extract_preds_pd['Extracted Aspect Terms'])
true_aspect_terms = np.array(extract_preds_pd["True Aspect Terms"])

print("Percentage of Extractions that are correct for the Test Data: ")
print(100 * (sum(pred_aspect_terms == true_aspect_terms) / test_data.shape[0]), " %")


# SubTask 2: Sentiment Polarity Classifier

# Weill use polarity frequency to classify our test data

sentiment_classifier = defaultdict(lambda : defaultdict(lambda : 0))

for row in train_data.itertuples():
	aspect_term = row[3]
	aspect_polarity = row[4]

	sentiment_classifier[aspect_term][aspect_polarity] += 1

sentiment_preds = []
sentiment_truths = []

for row in test_data.itertuples():
	aspect_term = row[3]

	if aspect_term not in terms_bank:
		sent_pred = "missing"

	else:
		classifier = sentiment_classifier[aspect_term]
		sent_pred = max(classifier, key = classifier.get)

	sentiment_preds.append(sent_pred)
	sentiment_truths.append(row[4])

sentiment_preds = np.array(sentiment_preds)
sentiment_truths = np.array(sentiment_truths)

print()
print("Percentage of Aspect Sentiment Classification that are correct for the Test Data: ")
print(100 * (sum(sentiment_preds == sentiment_truths) / test_data.shape[0]), " %")
