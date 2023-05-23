### WEB SCRAPING FOR AFRICAN LANGUAGES

# import packages
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# directory path
d_path = "C:\\Users\Acer\Desktop/"


#Initialize web url
web_path= "https://hadithi.africa/a-guide-to-african-languages-listed-by-country/"

#read in webpage
page = requests.get(web_path).content

# make a soup from the webpage
soup = bs(page, 'html.parser')


#it can be easily seen from webpage inspection that texts containing our needed data are in 'h3' and 'p' tags and arranged in 
#alternate manner.
# locate and grab all element tags containing required informatio

p = soup.find('h3', class_= "wp-block-heading").find_previous_sibling()
pre_needed = p.find_next_siblings()

country = []
official_language= []
other_language = []


#This loop will break on a certain 'h' tag which comes just after the last 'p' tag
# Official language details are within 'strong' elements. Other language information within parent 'p' tag
for i in pre_needed:
	if i.name == 'h3':
		country.append(i.text.strip())
	elif i.name == 'p':
		if i.strong:
			official_language.append(i.strong.text.strip())
		other_language.append(i.text.strip())
	else:
		break

#There are 54 countries. 54 elements are expected ineach list.
print(len(country), len(official_language), len(other_language))
(54, 54, 57)

# This suggests extra 'p' tags
for i in range(1, len(pre_needed), 2):
    if pre_needed[i].name != 'p':
        print("'p' tag not at index position: ", i)
        break


# an extra 'p' tag is found at end of the page another (and empty) 'p' tag within as well

# 			WRANGLING

other = other_language.copy()
l = other[-1]
print(l)


l2 = other[-2]


l3 = l2+" "+l
print(l3)


other[-2]= l3

other[-1]= ''

for i in range(len(other)):
	if "South Africans" in other[i]:
		print("South Africa found at index: ", i)
	if len(other[i])<1:
		print("Empty string at: ", i)

		

print(other[47])

print(other[46])


south_africa = other[46]+' '+other[47]
print(south_africa)


other[46] = south_africa
other[47] = ''

print(other[47])

print(other[46])

other = [i for i in other if len(i)>0]


		
print("Lenght of other: ", len(other))



# lenght of 54 indicates necessary correction has been made


# Extract language information from 'official_language' and 'other_language' list
# The following languages were search for; 'English', 'French', 'Yoruba', 'Arabic', 'Swahili', 'Portuguese', 'Spanish', 'Hausa'

language_options = ['English', 'French', 'Yoruba', 'Arabic', 'Swahili', 'Portuguese','Hausa', 'Spanish']


official_languages = []
for official in official_language:
	string = ''
	for language in language_options:
		if language in official:
			string = string+language+', '
	if string:
		official_languages.append(string[:-2])          # to remove extra ', ' character at end of string
	else:
		official_languages.append(string)               # to append an empty string



# inspect created 'official_languages'
print(official_languages[4])

print(official_languages[28])






#                   Extract language information from 'other2' list

other_languages=[]

for i in other:
	string = ''
	for language in language_options:
		if language in i:
			string = string+language+', '
	if string:
		other_languages.append(string[:-2]) # to remove extra ', ' character at end of string
	else:
		other_languages.append(string)       # to append an empty string

print(len(country), len(official_languages), len(other_languages))

#                   Create dataframe (relational table) from gathered information
Country_languages = pd.DataFrame(dict(Country = country, Official_languages = official_languages, Other_languages = other_languages))

#                   Inspect dataframe
Country_languages.head()



#			WRITE TO DISK

Country_languages.to_csv(d_path+"Country_languages.csv" ,index= False)



