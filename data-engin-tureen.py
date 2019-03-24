import xml.etree.ElementTree as ET # Import XML parser library
import pandas as pd # import Pandas library

# Read in XML data
# tree = ET.parse('../SemEval_14_Train/Restaurants_Train_v2.xml')
tree = ET.parse('../SemEval_14_Train/play.xml')
root = tree.getroot()

print(root)

# The data is nested like a tree because it's in XML format

# We will loop through all of the sentences (reviews)
# The whole XML data is nested under the root term: sentences
# This root has branches named "sentence" (individual review) and we have multiple of these

for sen in root.findall("sentence"):
	print(sen.tag)
	print(sen.attrib)

# code structure courtesy of Peter Min
# labeled_reviews = []
# for sentence in root.findall("sentence"):

#     entry = {}
#     aterms = []
#     aspects = []
#     if sentence.find("aspectTerms"):
#         for aterm in sentence.find("aspectTerms").findall("aspectTerm"):
#             aterms.append(aterm.get("term"))
#     if sentence.find("aspectCategories"):
#         for aspect in sentence.find("aspectCategories").findall("aspectCategory"):
#             aspects.append(aspect.get("category"))
#     entry["text"], entry["terms"], entry["aspects"]= sentence[0].text, aterms, aspects
#     labeled_reviews.append(entry)


# labeled_df = pd.DataFrame(labeled_reviews)
# print("there are",len(labeled_reviews),"reviews in this training set")
#    print(sentence.find("aspectCategories").findall("aspectCategory").get("category"))

