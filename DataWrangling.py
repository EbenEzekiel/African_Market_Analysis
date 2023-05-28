### WRANGLING ALL DATA INTO A SINGLE DATA READY FOR EXPLORATORY ANALYSIS

# import packages
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup as bs
import plotly.express as px

# working directory
d_path = "./data_folder/"


## import csv documents
# imf data on population, gross domestic product and gross domestic product per capita
imf_data = pd.read_csv(d_path+"imf_df.csv")


# World bank data on ease of doing buisness
ease_of_doing_buisness = pd.read_csv(d_path+"ease_of_doing_buisness.csv")

# World bank data on Consumption expenditure
consumption_expenditure = pd.read_csv(d_path+"consumption_expenditure.csv")

# information on languages
lang = pd.read_csv(d_path+"Country_languages.csv")

# African Union information on countryies by region
region = pd.read_csv(d_path+"african_countries_region.csv")


# rename columns of "consumption_expenditure" table
consumption_expenditure.columns = ["Country", "Consumption_expenditure(year)","Consumption_expenditure(%, value)" ]



#		    	INSTANTIATE EMPTY DATA FRAME OBJECT AS 'DATA'
data = pd.DataFrame()

#		    		WRANGLING "imf_data" into "data"
# inspect imf_data
imf_data.head()

imf_data.columns.to_list()


# Extract information from imf_data
imf_population = imf_data[imf_data["Subject Descriptor"] == 'Population'][["Country", "2022"]]
imf_population.reset_index(drop = True, inplace = True)


imf_GDP = imf_data[imf_data["Subject Descriptor"] == 'Gross domestic product, current prices'][["2022"]]
imf_GDP.reset_index(drop = True, inplace = True)


imf_GDP_per_capita = imf_data[imf_data["Subject Descriptor"] == 'Gross domestic product per capita, current prices'][["2022"]]
imf_GDP_per_capita.reset_index(drop = True, inplace = True)


#  inspection of imf_data shows population Units are in persons and value Scales in millions
imf_data[imf_data['Subject Descriptor']== "Population"]['Units'].unique()
imf_data[imf_data['Subject Descriptor']== "Population"]['Scale'].unique()

# inspection of imf_data shows GDP Units are in $USD and value Scales in billions
imf_data[imf_data['Subject Descriptor']== "Gross domestic product, current prices"]['Units'].unique()
imf_data[imf_data['Subject Descriptor']== "Gross domestic product, current prices"]['Scale'].unique()

# inspection of imf_data shows GDP per capita Units are in $USD and value Scales in units
imf_data[imf_data['Subject Descriptor']== "Gross domestic product per capita, current prices"]['Units'].unique()
imf_data[imf_data['Subject Descriptor']== "Gross domestic product per capita, current prices"]['Scale'].unique()



#			SET "imf_data" DATA ON POPULATION, GDP AND GDP PER CAPITA INTO "data"
data[["Country", "Population(Millions, 2022)"]] = imf_population
data[["GDP(USD Billions, 2022)"]] =imf_GDP
data[["GDP_per_capita(USD, 2022)"]] =imf_GDP_per_capita





#           FIND AND CORRECT INCONSISTENT FORMATTED COUNTRY NAMES IN COLUMNS
##            WE START BY DEFINING USEFUL FUNCTIONS 


# A function to identify values within a column and relace it with another given value
def colreplacer(df , dic, col= '', how = "loc"):
	# Make copy of dataframe to work with
	ddf= df.copy()
	ddf.index = ddf[col]  # set index to column for easy manipulation
	r = []
	for k in dic:
		if k in list(ddf.index):
			ddf.loc[k, col] = dic[k]
		else:
			r.append(k)
	#Set new value into 
	ddf.index = df.index
	if len(r)>0:
		print(f"These values in dataframe were not replaced : {r}.")
		return ddf
	else:
		print("All values set")
		return ddf
		
		
# A function to identify country names found in "obj" but not in "subj" arguments
def coldiff(obj, subj):
	obj = list(obj)
	subj = list(subj)
	return list(np.setdiff1d(obj, subj))


# A FUNCTION WHICH ACCEPTS A LIST OF STRINGS ARGUMENT TO SEARCH THROUGH COLUMNS
def searcher(obj, itr):
	results=[]
	for i in itr:
		i_s = str(i)
		j_list = []
		for j in obj:
			if re.search(j, i_s):
				j_list.append('Y')
			else:
				j_list.append('N')
		if list(pd.Series(j_list).unique()) == ['Y']:
			results.append(i)
	if len(results)==1:
		return results[0]
	return results
                
                
##          HANDLING COUNTRY NAME MISS-MATCH IN TABLES. OTHER TABLES WILL BE MERGED WITH ''data' TABLE
#           FOR 'ease_of_doing_buisness' TABLE
ease_of_doing_buisness.info()
ease_of_doing_buisness_miss_match = coldiff(data.Country, ease_of_doing_buisness.Region)

# string list to use in searching through 'ease_of_doing_buisness.Region' for each Country name miss-match
search_strings= [['oire'], ['Dem', 'Rep', 'Congo'], ['gypt'], ['Congo, Rep'], ['ipe', 'Tom'], ['Gambia']]

ease_of_doing_buisness_values = []

count = 0
for i in range (len(ease_of_doing_buisness_miss_match)):
    ease_of_doing_buisness_values.append(searcher(search_strings[count], ease_of_doing_buisness.Region))
    count+= 1

dic= dict(zip(ease_of_doing_buisness_values, ease_of_doing_buisness_miss_match))

# Replace values in 'ease_of_doing_buisness.Region' with values from 'data.Country'
ease_of_doing_buisness = colreplacer(ease_of_doing_buisness, dic, 'Region')

    
#            FOR 'LANG' TABLE
lang.info()
# get values in 'data.Country' but not not in 'lang.Country'
lang_miss_match = coldiff(data.Country, lang.Country)

# string list to use in searching through 'lang.Country' for each Country name miss-match
search_strings= [['erde'], ['oire'], ['Dem', 'Rep', 'Congo'],['tini'], ['Gambia']]


# identify corresponding values in lang.Country
lang_values = []
count = 0
for i in range (len(lang_miss_match)):
    lang_values.append(searcher(search_strings[count], lang.Country))
    count+= 1



dic= dict(zip(lang_values, lang_miss_match))

# replace appropriate values in 'lang' table
lang = colreplacer(lang, dic, 'Country')



#		  		            FOR 'consumption_expenditure' TABLE
consumption_expenditure.info()
#identify values in 'data.Country' but not in 'consumption_expenditure.Country'
consumption_expenditure_miss_match = coldiff(data.Country, consumption_expenditure.Country)

# string list to use in searching through 'consumption_expenditure.Country' for each Country name miss-match
search_strings= [['oire'],['Dem', 'Congo'],['Egypt'],['Congo, Rep'],['cipe'],['Gambia']]

# identify corresponding values in lang.Country
consumption_expenditure_values = []
count = 0
for i in range (len(consumption_expenditure_miss_match)):
    consumption_expenditure_values.append(searcher(search_strings[count], consumption_expenditure.Country))
    count+= 1
dic = dict(zip(consumption_expenditure_values, consumption_expenditure_miss_match ))
consumption_expenditure = colreplacer(consumption_expenditure, dic, "Country")




#                   FOR REGION TABLE
region.info()
#identify values in 'data.Country' buy not in 'region.Country'
region_miss_match = coldiff(data.Country, region.Country)

# string list to use in searching through 'region.Country' for each Country name in 'region_miss_match'
search_strings= [['oire$'], ['DR', 'Congo'], ['Congo', 'Rep'], ['Gambia']]

# identify corresponding values in region.Country
region_values = []
count = 0
for i in range (len(region_miss_match)):
    region_values.append(searcher(search_strings[count], region.Country))
    count+= 1
dic = dict(zip(region_values, region_miss_match ))

region=colreplacer(region, dic, "Country")



#		            Data Merging

ddata = data.merge(ease_of_doing_buisness[["Region", "Ease_of_DB_2020"]], left_on="Country" , right_on="Region", how = 'left')

#drop the 'region' column coming from the IMF data
ddata.drop('Region', axis = 1, inplace =True)

ddata = ddata.merge(lang, on="Country" , how = 'left')
ddata = ddata.merge(consumption_expenditure, on ='Country', how ="left")
ddata = ddata.merge(region, on='Country', how ="left")

ddata.info()

# Convert the "GDP_per_capita(USD, 2022)" column from object to float
float_val = [float(i.replace(',','')) for i in ddata["GDP_per_capita(USD, 2022)"]]
ddata["GDP_per_capita(USD, 2022)"] = float_val


# Write final data to disk
ddata.to_csv(d_path+"data.csv", index=False)
