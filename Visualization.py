import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, dash_table

import matplotlib.pyplot as plt
print('importing packages')
#-- ML models

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline

#--------------------------------------------------------

d_path = "C:\\Users\Acer\Desktop/"

# Read in data
data = pd.read_csv(d_path+"data.csv")

# View data clolumns
columns = data.columns.to_list()


count = 0

if count<1:
    msg_loading, msg_10, msg_40, msg_60, msg_90, msg_std = "Starting application...", 'loading; 10% complete...', 'loading; 40% complete...', 'loading; 60% complete...', 'loading; 90% complete...', '... application started.'
else:
    msg_loading, msg_10, msg_40, msg_60, msg_90, msg_std = "", '', '', '', '', '... application restarted.' 

if count<0:
    count = count+1
else:
    pass

def msg_printer(arg):
    if len(arg) >3:
        print(arg)
        
msg_printer(msg_loading)

#                                       POPULATION ANALYSIS

least_pop = data[["Country", "Population(Millions, 2022)"]].sort_values(by ="Population(Millions, 2022)"
        ).head(10).sort_values(by ="Population(Millions, 2022)", ascending = False)

top_pop = data[["Country", "Population(Millions, 2022)"]].sort_values(by ="Population(Millions, 2022)", ascending = False
        ).head(10).sort_values(by ="Population(Millions, 2022)")

# Viewing countries by population

fig_least_pop = px.bar(least_pop, x = "Country", y="Population(Millions, 2022)", title = "Countries with Lowest Population Figures")

fig_top_pop = px.bar(top_pop, x = "Country", y="Population(Millions, 2022)", title = "Countries with Highest Population Figures")

#fig_least_pop.show()
#fig_top_pop.show()

msg_printer(msg_10)


#                               EASE OF DOING BUISNESS ANALYSIS

least_Ease_of_DB = data[["Country","Ease_of_DB_2020"]].sort_values(by = 'Ease_of_DB_2020'
    ).head(10).sort_values(by = 'Ease_of_DB_2020', ascending = False)
top_Ease_of_DB = data[["Country","Ease_of_DB_2020"]].sort_values(by = 'Ease_of_DB_2020', ascending = False
    ).head(10).sort_values(by = 'Ease_of_DB_2020')

# View data
fig_least_Ease_of_DB = px.bar(least_Ease_of_DB, x = "Country", y = "Ease_of_DB_2020",
    title = "Countries with Poorest Ease of Doing Buisness Score")
fig_top_Ease_of_DB = px.bar(top_Ease_of_DB, x = "Country", y = "Ease_of_DB_2020", 
    title = "Countries with Most Impressive Ease of Doing Buisness Score")

#fig_least_Ease_of_DB.show()
#fig_top_Ease_of_DB.show()






#                           INTERACTIVE EASE OF DOING BUISNESS HISTOGRAM PLOT
eodb_hist = px.histogram(data[["Ease_of_DB_2020"]], x= "Ease_of_DB_2020", nbins = 12, title = "Ease of Doing Buisness Distribution")
#eodb_hist.show()

# Line plot
temp_data = data[["Ease_of_DB_2020", "Country"]].sort_values(by= "Ease_of_DB_2020")
eodb_line = px.line(temp_data, x= "Country", y= "Ease_of_DB_2020",
		    title ="Ease of Doing Buisness Score (From lowest to Highest Score)")
            
#eodb_line.show()


msg_printer(msg_40)




#                                  GDP ANALYSIS

least_gdp = data[["Country", 'GDP(USD Billions, 2022)']].sort_values(by ="GDP(USD Billions, 2022)"
        ).head(10).sort_values(by ="GDP(USD Billions, 2022)", ascending = False )

top_gdp = data[["Country", 'GDP(USD Billions, 2022)']].sort_values(by ="GDP(USD Billions, 2022)",
        ascending = False).head(10).sort_values(by ="GDP(USD Billions, 2022)")

# View data
fig_least_gdp = px.bar(least_gdp, x= "Country", y= "GDP(USD Billions, 2022)", title = "Countries with Lowest GDP")
fig_top_gdp = px.bar(top_gdp, x= "Country", y= "GDP(USD Billions, 2022)", title = "Countries with Highest GDP")

#fig_least_gdp.show()
#fig_top_gdp.show()





#                               GDP PER CAPITA ANALYSIS
least_gdp_per_c = data[["Country", "GDP_per_capita(USD, 2022)"]].sort_values(by ="GDP_per_capita(USD, 2022)" 
        ).head(10).sort_values(by ="GDP_per_capita(USD, 2022)", ascending = False )
top_gdp_per_c = data[["Country", "GDP_per_capita(USD, 2022)"]].sort_values(by ="GDP_per_capita(USD, 2022)", 
        ascending = False).head(10).sort_values(by ="GDP_per_capita(USD, 2022)")

# View data
fig_least_gdp_per_c = px.bar(least_gdp_per_c , x= "Country", y = "GDP_per_capita(USD, 2022)",
                title = "Countries with lowest GDP Per Capita")
fig_top_gdp_per_c = px.bar(top_gdp_per_c , x= "Country", y = "GDP_per_capita(USD, 2022)", 
                title = "Countries with Best GDP Per Capita")

#fig_least_gdp_per_c.show()
#fig_top_gdp_per_c.show()



msg_printer(msg_60)



#                                   CONSUMER EXPENDITURE DATA ANALYSIS

least_exp = data[["Country", "Consumption_expenditure(%, value)"]].sort_values(by = "Consumption_expenditure(%, value)"
            ).head(10).sort_values(by = "Consumption_expenditure(%, value)", ascending= False)
top_exp = data[["Country", "Consumption_expenditure(%, value)"]].sort_values(by = "Consumption_expenditure(%, value)",
            ascending = False ).head(10).sort_values(by = "Consumption_expenditure(%, value)" )

#View data
fig_least_exp = px.bar(least_exp, x = "Country", y = "Consumption_expenditure(%, value)",
            title = "Countries with Lowest Consumption_expenditure")
fig_top_exp = px.bar(top_exp, x = "Country", y = "Consumption_expenditure(%, value)",
            title = "Countries with Highest Consumption_expenditure")

#fig_least_exp.show()
#fig_top_exp.show()




#                                       REGIONAL ANALYSIS
region_group = data.groupby('Region').sum()
region_group['Region']= region_group.index
region_group['GDP_per_capita(USD, 2022)'] =  list((region_group['GDP(USD Billions, 2022)']/region_group['Population(Millions, 2022)'])*10**3)



options_values = ['Population(Millions, 2022)', 'GDP(USD Billions, 2022)', 'GDP_per_capita(USD, 2022)' ]


misc_options= ['Population(Millions, 2022)', 'GDP(USD Billions, 2022)', 'GDP_per_capita(USD, 2022)', 'Ease_of_DB_2020', 'Consumption_expenditure(%, value)']
misc_options2 = ['Population(Millions, 2022)', 'GDP(USD Billions, 2022)', 'GDP_per_capita(USD, 2022)', 'Ease_of_DB_2020', 'Consumption_expenditure(%, value)']



########################        MACHINE LEARNING        ################################################

print(""" 
    training models...
""")

# Make pipeline and instantiate KMeans and StandardScaler within the pipe
pipe = make_pipeline(MinMaxScaler(), KMeans(n_clusters = 4))

# select data types for model training
ml_df = data.select_dtypes('number')

# drop 'Consumption_expenditure(year)' column. It is not needed
ml_df.drop(['Consumption_expenditure(year)', 'Consumption_expenditure(%, value)'], axis = 1, inplace =True)


# fit model, # drop 'Country' column
pipe.fit(ml_df)

# get labels from trained model
label = pipe['kmeans'].labels_

# include labels in ml_data
ml_df = data.copy()
ml_df['Label'] = label


#-------------------------------------------------------------------------



ml_options_value = ['Population(Millions, 2022)', 'GDP(USD Billions, 2022)', 'GDP_per_capita(USD, 2022)', 'Ease_of_DB_2020']


# -----------------------------------------------------------------------------------------------------------------------------

app = Dash(__name__)

app.layout= html.Div([
html.Br(),
html.H2("BUISNESS AND INVESTMENT PROSPECTS OF AFRICAN COUNTRIES"),
html.Br(),
dash_table.DataTable(data= data.to_dict('records'), page_size = 11, style_table = {'width':'50%'} ),
html.Br(),
html.P("In this analysis, for each indicator of interest, we shall focus on 10 best performing and 10 least performing Countries"),
html.Br(),
html.H4("Population :"),

    html.Div([html.P("""We shall begin with population analysis. The more the number of potential consumers for goods and services the more likely
        a buisness will make profitable sales and remain open.
        """),
        html.P('Nigeria, followed by Egypt take the lead.'),
        
        
    dcc.Graph(id = 'least population', figure = fig_least_pop ),
    dcc.Graph(id = 'top population', figure = fig_top_pop)
    ]), html.Br(),
    

html.Div([
    html.H4("Ease of Doing Buisness (E_of_DB)"),
    html.P(""" 
    A number of hurdles must be crossed by an investor before commencing buisness operations and remain in buisness from day
    to day. These includes ease of buisness registration, power availability, good credit facilities, good roads and other 
    social ammenities and facilities to mention a few.
    """),
    html.P("A good ease of doing buisness score means that buisnesses are more likely to survive."),
    html.P("""
    Mauritius and Rwanda take the lead with scores higher than many more developed countries in the world.
    Somalia and Eritrea offer the least conducive environment
    """),
    html.P('These are Africas worse and best performers.'),
    
    dcc.Graph(id = 'least eodb', figure = fig_least_Ease_of_DB ),
    dcc.Graph(id = 'top eodb', figure = fig_top_Ease_of_DB),html.Br(),
    dcc.Graph(id = 'eodb hist', figure = eodb_hist),
    dcc.Slider(10,14,1, value = 12, id = 'eodb slider' ), html.Br(),
    dcc.Graph(id = 'eodb line', figure = eodb_line)
    ]),
    
html.Div([
    html.H4("National Gross Domestic Product (GDP) Value "),
    html.P("""
    The national GDP is an indicator of how healthy the buissness community is. Higher population usually imply higher GDP.
    Availability of natural resources (positively) influence this indicator too. Natural resources availability implies
    proximity to raw materials.
    """ ), 
    html.P("""
    It is not suprising that Nigeria and Egypt take the lead as they have the highest populations. South Africa, though
    much less populated compared to Nigeria, has an impressive GDP. This too is not surprising as it is the most developed and 
    industrialised African nation
    """),
    html.P('These are Africas worst and best performers'),
    dcc.Graph(id = 'least gdp', figure = fig_least_gdp),html.Br(),
    dcc.Graph(id = 'top gdp', figure = fig_top_gdp)
]), html.Br(),



    
html.Div([
    html.H4(" Gross Domestic Product Per Capita (GDPPC) "),
    html.P("""This is an indicator of average productivity of a country's populace. It is obtained by dividing the
    country's GDP by its population. It is an indicator of average purchasing power"""),
    dcc.Graph(id= 'least gdppc', figure =  fig_least_gdp_per_c),
    dcc.Graph(id= 'top gdppc', figure =  fig_top_gdp_per_c),
    html.P("""
    The gross domestic product per capita shows a rather surprising result. Seychelles, a country of about 100,000 people and 
    also (not suprisingly) having one of the lowest total gross domestic product values ranks the highest in terms of gross domestic
    product per capita. Equatorial Guinea and Gabon also surprisingly doing well on the continent beating countries such as 
    Nigeria, Egypt and South Africa, countries with larger population and gross domestic products
    """),
    ]),
    
    

html.Div([
    html.H4(" Consumer Expenditure "),
    html.P("""This is an indicator of a country's consumer contribution to the economy's GDP.
    Represented as percentage contribution in this study.
    """),
    dcc.Graph(id= 'least cons_exp', figure =  fig_least_exp),
    dcc.Graph(id= 'top cons_exp', figure =  fig_top_exp)
    ]),
html.Br(),html.Br(),




    
html.Div([
    html.H4(" Country specific analysis "),
    html.B("Nigeria"),
    html.P("""
    Nigeria, the most populous and largest African economy happens to rank 22nd in terms of GDP per capita of about $2,300 per annum.
    This country will be a good market for testing acceptance of new products on the African continent and a good target for middle class products
    and services
    """), html.Br(),
    html.B("South Africa"),
    html.P("""
    Africa's most industrialized country and third largest economy. Like Nigeria, South Africa is a potential market for middle class
    products and services. It however has a GDP per capita value of about $6,700 per annum which makes it a potential market for luxury
    goods and services
    """), html.Br(),
    html.B("seychellles"),
    html.P("""
    Seychelles is a country in the Southern region of Africa. It has the most impressive GDP per capita of about $20,000 per annum and 
    a small population (slightly less than one hundred thousand). This makes it a potential luxury holiday location and a target for 
    luxury goods and services market. Real estate investments could also prove profitable in this location
    """),
    html.Br(),
    html.B("Mauritius"),
    html.P("""
    In this study we found Mauritius to have the best ease of doing buisness index of about 80 points, the best in Africa.
    It has a comparatively inpressive GDP per capita figure too. The small population is however a potential downside to large scale investment
    here.
    """)
    ]),
    html.Br(),
    html.Br(),
    
    

    # Dropdown menu and regional analysis
    html.Div([
    
    html.H4("Here we take a look at regional indicators in population, GDP and GDP per capita"),
    html.Br(), html.Br(),
    dcc.Dropdown(options_values, options_values, style= {'width': '50%' }, id= 'dropdown', placeholder= 'Select a variable' ),
            html.Br(), html.Br(),
            
    dcc.Graph(id = 'multigraph', figure = {}),

        ]),

    html.Div([
    html.H4(" Regional Analysis "),
    html.B('West Africa'),
    html.P("""
    Population wise, West Africa, the most populous region is suprisingly about 40 million people ahead of East Africa, the second most populous region
    suggesting that the majority of West Africa's population size comes from Nigeria. This emphasizes the country's regional power and potential
    in trade and commerce
    """),
    html.B('North Africa'),
    html.P("""
    Although the third most populous region, it has the highset GDP and GDP per capita by region. This is an idicator of bestter productivity amongst these countries compared to 
    other African countries
    """), html.Br(),
    
    html.B('Southern Africa'),
    html.P("""
    Africa's second best performing region in GDP per capita figures. Although it has a combined population of about 193 million people
    (fourth in Africa) it has an impressive GDP performance. This may be due to the highly industrialized nature of the region.
    """),
    
    html.Br(),
    html.B('East Africa'),
    html.P("""
    Africa's second most populous region but low in GDP and GDP per capita figures of about $455 billion and $1,186 respectively. This region will likely be good market for low cost productcs.
    """),
    
    html.Br(),
    html.B('Central Africa'),
    html.P("""
    The Central African region ranks 5th in population size, GDP and GDP per capita within the continent. These suggest that the region
    is grossly under developed and will require intense human resource investment to get appreciable buisness investment returns from the region.
    In the absence of security and political uncertainties, it may however be a source of cheap labour and production site to manufacture goods
    which will be exported to neighbouring and more economically vibrant regions.
    """)    
    
    
    ]),
    html.Br(), html.Br(),

#####################################     MACHINE LEARNING VISUALS       ###########################################

html.P("""
    We used a clustering machine learnng model to check what interesting facts we can obtain from our data. We used population, Ease
    of doing buisness, GDP and GDP per capita values for our machine learning model.
"""),
html.P("""We identified four clusters which can easily be spotted from the "Population vs. Ease of doing buisness" graph below"""),
html.H6("x-axis variable"),
dcc.Dropdown(ml_options_value, ml_options_value, style= {'width': '50%' }, id= 'ml_dropdown1', placeholder= 'Select a variable' ),
html.H6("y-axis variable"),
dcc.Dropdown(ml_options_value, ml_options_value, style= {'width': '50%' }, id= 'ml_dropdown2', placeholder= 'Select a variable' ),
dcc.Graph(id = 'ml_graph', figure = {}),

html.P("""
    On the "Population vs. Ease of doing buisness" graph, we see countries clustered some to the top right corner, some to the
    lower right corner and others to the lower left corner."""),
html.P(""" From our clusters, it can be concluded that:
"""),
html.P(""" 1. Nigeria, Egypt and South Africa are the largest and overall best performing economies on the continent. Cluster label 0.
"""),
html.P(""" 2.  Seychelles, Gabon and Equatorial Guinea are the most productive per capita. Cluster label 3. Easily seen from the "GDP per
    capita vs. GDP  graph". This makes these countries potential targets for luxury products and services.
"""),

html.P(""" 3.  Countries within cluster label 2 can be said to be Countries of least investment prospects
"""),
html.P(""" 4.  Countries within cluster label 1 can be said to be Countries of moderate investment prospects
"""),
html.Br(),
dash_table.DataTable(data= ml_df[['Country','Label']].sort_values(by = 'Label').to_dict('records'), page_size = 11, style_table = {'width':'50%'} ),
html.Br(),html.Br(),


html.H4('Here we come to the end of the analysis. Thank you.'),
html.Br(),html.Br(),

#####################################        MISCELLANEOUS            #########################################
html.H3('Miscellaneous', style={'position':'center'}),
html.Div([    
    html.H4("Line graphs"),
    html.Br(), 
    dcc.Dropdown(misc_options, misc_options, style= {'width': '50%' }, id= 'misc_dropdown', placeholder= 'Select a variable' ),
            html.Br(), html.Br(),
            
    dcc.Graph(id = 'misc_line_graph', figure = {})
        ]),


html.Div([
    html.H4("Bar plots"),
    html.Br(), html.Br(),
    dcc.Dropdown(misc_options2, misc_options2, style= {'width': '40%' }, id= 'misc_bar_dropdown1', placeholder= 'Select a variable' ),
    dcc.Dropdown(["10","20"], [10, 20], style= {'width': '40%' },
        id= 'misc_bar_dropdown2', placeholder= 'Select a variable' ),
    dcc.Dropdown(["Top", "Least"], ["Top", "Least"], style= {'width': '40%' },
        id= 'misc_bar_dropdown3', placeholder= 'Select a variable' ),    
        

            html.Br(), html.Br(),
            
    dcc.Graph(id = 'misc_bar_graph', figure = {}),
        ]),


# dcc.Dropdown(ml_options_value, ml_options_value, style= {'width': '50%' }, id= 'ml_dropdown1', placeholder= 'Select a variable' ),
# dcc.Dropdown(ml_options_value, ml_options_value, style= {'width': '50%' }, id= 'ml_dropdown2', placeholder= 'Select a variable' ),
# dcc.Dropdown(['Country', 'Region', 'Official_languages'], ['Country', 'Region', 'Official_languages'],
            # style= {'width': '50%' }, id= 'ml_dropdown3', placeholder= 'Select a variable' ),
# dcc.Graph(id = 'ml_graph', figure = {}),






#########################################     "FOOT NOTE"      #########################################


html.Br(),html.Br(),  
html.Div([
html.P("Data Used for this analysis were sourced from:"),
    html.P("The world Bank ;"),
        html.P('Ease of doing buisness, Consumption expenditure'),
        html.P('https://data.worldbank.org/indicator/NE.CON.TOTL.ZS'),
       html.P('https://archive.doingbusiness.org/en/data/doing-business-score'),
    html.P('IMF  ;'),
        html.P('Population, Gross Domestic Product, Gross Domestic Products Per Capita'),
        #https://www.imf.org/en/Publications/WEO/weo-database/2022/October/weo-report?c=612,614,638,616,748,618,624,622,626,628,632,636,634,662,611,469,642,643,734,644,646,648,652,656,654,664,666,668,672,674,676,678,682,684,686,688,728,692,694,714,716,722,718,724,726,199,733,732,738,742,744,746,754,698,&s=NGDPD,NGDPDPC,LP,&sy=2022&ey=2022&ssm=0&scsm=1&scc=0&ssd=1&ssc=0&sic=0&sort=country&ds=.&br=1
        
    html.P('Hadithi ;'),
        html.P('Languages in Africa'),

html.P("https://hadithi.africa/a-guide-to-african-languages-listed-by-country"),        
        ]),
        
        
# <!---------------------------------------------END ------------------------------------------------------------------>
])


msg_printer(msg_90)



@app.callback(
Output(component_id= "eodb hist", component_property="figure"),
Input(component_id = 'eodb slider', component_property = 'value')
)
def hist_slider(num):
    return px.histogram(data[["Ease_of_DB_2020"]], x= "Ease_of_DB_2020", nbins = num, title = "Ease of Doing Buisness Distribution")




@app.callback(
Output(component_id= "multigraph", component_property="figure"),
Input(component_id = 'dropdown', component_property = 'value')
)
def multi_grapher(arg):
    return px.bar( region_group, x= "Region", y= arg, title = f"Regional Graph: {arg}")

######################      ML      ##########################

@app.callback(
Output(component_id= "ml_graph", component_property="figure"),
Input(component_id = 'ml_dropdown1', component_property = 'value'),
Input(component_id = 'ml_dropdown2', component_property = 'value'),
)
def ml_grapher(arg1, arg2):
    return px.scatter( ml_df, x= arg1, y= arg2, title = f"Scatter plot of {arg2} vs. {arg1}.", color = 'Label', hover_name = 'Country')


########### MISCELLANEOUS

@app.callback(
Output(component_id= "misc_line_graph", component_property="figure"),
Input(component_id = 'misc_dropdown', component_property = 'value')
)
def misc_line_grapher(arg):
    return px.line(data.sort_values(arg), x= "Country", y= arg, title = f"Graph of {arg} by country")
    
    

@app.callback(
Output(component_id= "misc_bar_graph", component_property="figure"),
Input(component_id = 'misc_bar_dropdown1', component_property = 'value'),
Input(component_id = 'misc_bar_dropdown2', component_property = 'value'),
Input(component_id = 'misc_bar_dropdown3', component_property = 'value')
)
def misc_bar_grapher(arg, arg2, arg3):
    arg2 = int(arg2)
    if 'Least' in arg3:
        d= data.sort_values(arg)
        return px.bar(d.head(arg2).sort_values(arg, ascending = False), x= "Country", y= arg, title = f"Least {arg} by country")
    else:
        d= data.sort_values(arg, ascending= False)
        return px.bar(d.head(arg2).sort_values(arg) , x= "Country", y= arg, title = f"Top {arg} by country")


# @app.callback(
# Output(component_id= "ml_graph", component_property="figure"),
# Input(component_id = 'ml_dropdown1', component_property = 'value'),
# Input(component_id = 'ml_dropdown2', component_property = 'value'),
# Input(component_id = 'ml_dropdown3', component_property = 'value')
# )
# def ml_grapher(arg1, arg2, arg3):
    # fig = px.scatter( ddf, x= arg1, y= arg2, title = f"Scatter plot of {arg1} vs. {arg2}.", color = 'Label', hover_name = arg3)
    # return fig2



if __name__=="__main__":
    msg_printer(msg_std)
    print('\n', '\n')
    app.run_server(debug = True, port = 5000)














