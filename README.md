Machine Learning Approach to Study Food Recalls, User Generated Content and Food Borne illnesses
================================================================================================

Description
===========
The project is segrested into 4 phases.
1. **Phase-1**: Data Acquisition and Metadata Generation - March 15 2019
2. **Phase-2**: Setting Updata application pipeline - March 30 2019
3. **Phase-3**: Data Visualization - April 25 2019
4. **Phase-3**: Application Testing and Hostinng - May 28 2019

Phase-1
=======
1 in 8 people in Canada and 1 in 6 Americans get sick from contaminated food each year. The it Food borne illnesses are one of the biggest preventable public health problems in Canada and United States of America. In-line with Canadian Food Inspection Agencies strategic priorities of “Better use of our data, reports and surveillance to identify trends”. The project aims to analyze the food recall data for Canada and America to provide better insights into food recall trends, identify critical products and
geographies. With the open data initiative by Canadian and United States governments the food recall data is available as APIs. The food recalls data accessible through the APIs is semi structured and lack the required levels/hierarchy of information to drive the data analysis

This phase aims to use machine learning to generate the required metadata to support different levels of analysis. Some of the metadata that is planned to be generated includes

1. Product Category: The decryption of the recall includes the exact brand of the product that is being recalled. The API metadata does not specify the category of the product.
Ex: Eat Smart brand Salad Shake Ups. This information is too granular for analysis. A better level of analysis would be at product category. Ex: Ready to Eat or Froze foods or Vegetables

2. Specific Reason for Recall: In cases where the reason for recall is not Microbiological or Allergen the exact reason is not specified in the API metadata. Ex: Microbiological – Salmonella vs Extraneous Material. In case of Microbiological the exact reason for recall is provided as Salmonella while Extraneous Material does not have such information. The same information is provided in the text “Uruthira brand Hand Pounded Red Rice recalled due to presence of sand (rocks)”

Related Work
------------
The problem to generate metadata can be viewed as document classification problem for generating product category and key phrase extraction problems. Early research on document classification were based on Bayesian Classification approach as studied by Andrew K McCallum in which multiple classes that comprise a document were represented by a mixture model. As early as 2000, neural networks have been suggested by Dieter Merkl for document classification. More recent studies by Pei-Yi Hao in 2006 suggest an SVM based model for automatic categorization of documents into pre-defined topic hierarchies where ‘global context information’, has been used in conjunction with ‘local context information’. On the other hand, early works on key word extraction include SVM based model as suggested by Kuo Zhang in 1999.

Data Sources
------------
The data will extracted from the publicly available APIs

1. Government of Canada: http://healthycanadians.gc.ca/recallalert-rappel-avis/api/{recall_id}/en)
2. United States of America: https://open.fda.gov/apis/food/enforcement/download/

The response of the APIs is in JSON format. The responses have many fields fields, but the features which believe will be valuable to the redictive model are ”alert sub-type”, ”type of
communication”, ”distributed provinces”, ”extent of distribution”, ”subcategory”, ”background” and ”affected products”.

For creating a training dataset with labelled data,

the United States Nutrition Database: https://ndb.nal.usda.gov/ndb/search/
is used in conjunction with publicly available Walmart API: http://api.walmartlabs.com/v1/search?piKey={API_Key}={S}

===========

pipenv shell
pipenv install ipykernal
ipython kernel install --user --name=phronesis
jupyter notebook

Test using PyCharm

Note
====

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
