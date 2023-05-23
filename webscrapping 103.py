### WEB SCRAPING OF AFRICAN UNION SITE FOR REGIONAL GROUPS OF EACH COUNTRY

import pandas as pd
import numpy as numpy
import requests
from bs4 import BeautifulSoup


d_path = "C:\\Users\Acer\Desktop/"   # path to working directory

web_url = "https://au.int/en/member_states/countryprofiles2"


page = requests.get(web_url).content

soup = BeautifulSoup(page, 'html.parser')

soup.find('div', class_= "field-item even")

div_l = soup.find_all('div', class_= "field-item even")


for i in range(len(div_l)):
	if div_l[i].table:
		j=i
		print(i)


#   WRITE HTML STRING TO DISK
with open(d_path+'temp.html', 'w')as f:
	f.write(str(div_l[j]))

#   READ HTML STRING FROM DISK WITH PANDAS
pd_t = pd.read_html(d_path+"temp.html")

# obtain region information from site and assign to each frame

central_africa = pd_t[0][[1]]
central_africa["Region"] = ["Central Africa"]* len(central_africa)


east_africa = pd_t[1][[1]]
east_africa["Region"] = ["East Africa"]* len(east_africa)

north_africa = pd_t[2][[1]]
north_africa["Region"] = ["North Africa"]* len(north_africa)

southern_africa = pd_t[3][[1]]
southern_africa["Region"] = ["Southern Africa"]* len(southern_africa)

west_africa = pd_t[4][[1]]
west_africa["Region"] = ["West Africa"]* len(west_africa)

df = pd.concat([central_africa, east_africa, north_africa, southern_africa, west_africa], axis = 0)

df.columns= ['Country','Region']

df.drop(df.loc[0].index, inplace = True)

df.to_csv(d_path+'african_countries_region.csv', index=False)






