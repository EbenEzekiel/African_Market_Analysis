### WEB SCRAPING OF IMF SITE FOR DATA ON POPULATION, GDP AND GDP PER CAPITA, 
### AND WORLD BANK SITE FOR CONSUMPTION EXPENDITURE AND EASE OF DOING BUISNESS DATA

# import packages
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os


# Path to working directory
d_path = "./data_folder/"

if not os.path.exists(d_path):
    os.makedirs(d_path)




# imf data on population and GDP
imf_web_path = "https://www.imf.org/en/Publications/WEO/weo-database/2022/October/weo-report?c=612,614,638,616,748,618,624,622,626,628,632,636,634,662,611,469,642,643,734,644,646,648,652,656,654,664,666,668,672,674,676,678,682,684,686,688,728,692,694,714,716,722,718,724,726,199,733,732,738,742,744,746,754,698,&s=NGDPD,NGDPDPC,LP,&sy=2022&ey=2022&ssm=0&scsm=1&scc=0&ssd=1&ssc=0&sic=0&sort=country&ds=.&br=1"

# Consumption expenditure data source: World bank
consumption_expenditure_web_path = "https://data.worldbank.org/indicator/NE.CON.TOTL.ZS"

# Ease of doing buisness. Source: World bank
ease_of_doing_buisness_web_path = "https://archive.doingbusiness.org/en/data/doing-business-score"


# make get request
page1= requests.get(imf_web_path).content
page2= requests.get(consumption_expenditure_web_path).content
page3= requests.get(ease_of_doing_buisness_web_path).content


#   MAKE SOUPS
soup1 = bs(page1, "html.parser")
soup2 = bs(page2, "html.parser")
soup3 = bs(page3, "html.parser")

# 			SCRAPE DATA FROM SOUP 1

div = soup1.find('div', class_ = "pane pane--table")
table = div.find("table", class_="fluid")

columns = [ i.text for i in table.find('thead').find('tr').find_all('th')]



df_body = []
for row in table.find('tbody').find_all('tr'):
	row_data = row.find_all('td')
	df_body.append([info.text for info in row_data])

	
imf_df = pd.DataFrame(df_body, columns = columns)
imf_df.head()



# 			SCRAPE DATA FROM SOUP 2
#		### Made use of html extract

extract_path = "./soup2extract.html"
	

#		READ IN HTML EXTRACT
with open (extract_path, 'r') as f:
	soup2 = bs(f.read(), 'html.parser')


countries = soup2.div

consumption_expenditure=[]

for country in countries.find_all('div'):
	m=[]
	for tag in country.find_all('div'):
		if len(tag.text.strip())> 3:
			m.append(tag.text.strip())
	if len(m)>0:
		consumption_expenditure.append(m)

		
columns = ["Country", "Most_Recent_year", 'Most_Recent_Value']

# Final Consumption Expendition(% of GDP) = consp_exp
consumption_expenditure= pd.DataFrame(consumption_expenditure, columns = columns)

consumption_expenditure.head()


#                    			SCRAPE DATA FROM SOUP 3
#		                       ### Made use of html extract

extract_path = "./soup3extract.html"

#	    	READ IN HTML EXTRACT
with open (extract_path, 'r') as f:
	soup3 = bs(f.read(), 'html.parser')


table = soup3.find('tbody')

ease_of_doing_buisness =[]

for tr in table.find_all('tr'):
	l=[]
	for td in tr.find_all('td'):
		l.append(td.text)
	ease_of_doing_buisness.append(l)


columns = ['','Region', 'Ease_of_DB_2019', 'Ease_of_DB_2020', '']

ease_of_doing_buisness = pd.DataFrame(ease_of_doing_buisness, columns= columns)


ease_of_doing_buisness = ease_of_doing_buisness[['Region', 'Ease_of_DB_2019', 'Ease_of_DB_2020']]




#                   WRITE ALL SCRAPPED DATA TO DISK


imf_df.to_csv(d_path+"imf_df.csv", index= False)

consumption_expenditure.to_csv(d_path+"consumption_expenditure.csv", index= False)

ease_of_doing_buisness.to_csv(d_path+"ease_of_doing_buisness.csv", index= False)


