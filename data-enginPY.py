# Import Libraries
import xml.etree.ElementTree as ET # To Parse the XML data
import pandas as pd # import Pandas library
import pickle # for pickling Python data structures
from collections import Counter

# Read in XML data (courtesy of SemEval 2014 committee)
tree = ET.parse('../SemEval_14_Train/Restaurants_Train_v2.xml')
# tree = ET.parse('../SemEval_14_Train/play.xml')
root = tree.getroot()

processed_reviews = [] # this list will contain dictionaries, eventually we will convert it to a Pandas DataFrame

for sen in root.findall("sentence"):
    # this dictionary will store the columns we are interested in storing for our processed dataset
    data_dict = {} 

    review = sen[0].text # assign the text review to this variable
    
    # We add this at the beginning of the for loop to avoid adding terms to reviews that don't have terms
    term_tokens = [] # slot 1 for value_container 
    term_pols = [] # slot 2 for value_container
    cat_tokens = [] # list of all of the labeled categories for the data
    cat_pols = [] # list of the associated polarities
    
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
    data_dict["Review_ID"] = sen.attrib["id"]
    data_dict["Review"] = review
    data_dict["Aspect_Term"] = term_tokens
    data_dict["Aspect_Polarity"] = term_pols
    data_dict["Aspect_Count"] = len(term_tokens)
    data_dict["Category"] = cat_tokens
    data_dict["Category_Polarity"] = cat_pols
    data_dict["Category_Count"] = len(cat_tokens)

    # each element in the following list will be a row for our processed dataset
    processed_reviews.append(data_dict) # append data_dict

reviews_pd = pd.DataFrame(processed_reviews)
print("Shape of Training data", reviews_pd.shape)
# reviews_pd.head(3)


col_reform = ['Review_ID', 'Review', 'Aspect_Term', 'Aspect_Polarity', 'Aspect_Count', 'Category', 'Category_Polarity', 'Category_Count']
reviews_pd = reviews_pd[col_reform]
reviews_pd.head(2)


print(sum(reviews_pd.iloc[:,4])) # the Aspect Count column
print(sum([len(x) for x in reviews_pd.iloc[:,2]])) # the Aspect Term column


print(sum(reviews_pd.iloc[:,7]))
print(sum([len(x) for x in reviews_pd.iloc[:,5]]))


# Let's see if there is an imbalance in the number of aspect terms we have and the aspect category
print(len(reviews_pd.iloc[0,2]) == len(reviews_pd.iloc[0,5]))
print(len(reviews_pd.iloc[1,2]) == len(reviews_pd.iloc[1,5]))


# make subsets of the data that have either more aspect terms or more categories then terms...
reviews_pd_MoreTerms = reviews_pd[reviews_pd.Aspect_Count > reviews_pd.Category_Count]
print(reviews_pd_MoreTerms.shape)

reviews_pd_MoreCats = reviews_pd[reviews_pd.Aspect_Count < reviews_pd.Category_Count]
print(reviews_pd_MoreCats.shape)

print(reviews_pd_MoreTerms.shape[0] + reviews_pd_MoreCats.shape[0])

# make subset of the data that has perfect balance
reviews_pd_Balance = reviews_pd[reviews_pd.Aspect_Count == reviews_pd.Category_Count]
print(reviews_pd_Balance.shape[0])


print(reviews_pd[reviews_pd.Category_Count == 0].shape[0])

reviews_pd_NoAspTerms = reviews_pd[reviews_pd.Aspect_Count == 0]
print(reviews_pd_NoAspTerms.shape[0])