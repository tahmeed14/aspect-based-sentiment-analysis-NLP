# Aspect-Based Sentiment Analysis: Findings from Unstructured Natural Language
# Tahmeed Tureen - University of Michigan, Ann Arbor

# data-engin-tureen.py
# Code to process the XML format dataset from 2014 SemEval Task 4

import xml.etree.ElementTree as ET # Import XML parser library
import pandas as pd # import Pandas library

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
		data_dict["Aspect Polarity"] = pols_list[i]

		aspects_data_list.append(data_dict)

# Convert to Pandas Data Frame for convenience
aspects_terms_pd = pd.DataFrame(aspects_data_list)
aspects_terms_pd = aspects_terms_pd[['Review', 'Review ID', 'Aspect Term', 'Aspect Polarity']] # re-order

# Save to a CSV for future use
path_csv = r"C:\\Users\\Tahmeed\\Dropbox\\Masters\\win-2019\\NLP_SI630\\final-project\\asba\\aspect-terms-data.csv"
aspects_terms_pd.to_csv(path_csv, index = None, header = True)







