# Aspect-Based Sentiment Analysis Code I
# Tahmeed Tureen - University of Michigan, Ann Arbor

import xml.etree.ElementTree as ET # Import XML parser library
import pandas as pd # import Pandas library

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
	#print(sen.tag)
	print(sen.attrib["id"])
	data_dict = {}

	review = sen[0].text # assign the text review to this variable
	print(review)
	print()

	if sen.find("aspectTerms"): # if there exists aspect terms in review 
		
		term_tokens = [] # slot 1 for value_container
		term_pols = [] # slot 2 for value_container
		# we make define these lists because a review can have multiple aspects

		# Iterate through individual aspect terms and strip its polarity
		for branch in sen.find("aspectTerms").findall("aspectTerm"):
			term = branch.get("term")
			term_polarity = branch.get("polarity")

			term_tokens.append(term)
			term_pols.append(term_polarity)

	# 		print(term)
	# 		print(term_polarity)

	# print(term_tokens)
	# print(term_pols)
	# print()

	if sen.find("aspectCategories"): # if there exists labeled categories

		cat_tokens = [] # slot 3 for value_container
		cat_pols = [] # slot 4 for value_container
		# We define these lists because a review can have multiple aspects

		for branch in sen.find("aspectCategories").findall("aspectCategory"):
			category = branch.get("category")
			cat_polarity = branch.get("polarity")

			cat_tokens.append(category)
			cat_pols.append(cat_polarity)

	# 		print(category)
	# 		print(cat_polarity)

	# print(cat_tokens)
	# print(cat_pols)

	data_dict["Review ID"] = sen.attrib["id"]
	data_dict["Review"] = review
	data_dict["Aspect"] = term_tokens
	data_dict["Aspect Polarity"] = term_pols
	data_dict["Category"] = cat_tokens
	data_dict["Category Polarity"] = cat_pols

	processed_reviews.append(data_dict)

reviews_data_pd = pd.DataFrame(processed_reviews)
print(reviews_data_pd)

path_csv = r"C:\\Users\\Tahmeed\\Dropbox\\Masters\\win-2019\\NLP_SI630\\final-project\\asba\\processed-reviews.csv"
# Save as a CSV for further use
reviews_data_pd.to_csv(path_csv, index = None, header = True)