########################################################
###        Imports and file's paths variables        ###
########################################################

# panda #
import pandas as pd

# plotly #
import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots

# plotly express #
import plotly_express as px

# os #
import os

# request #
import requests

# dash #
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output
from dash.dependencies import Input

# file's paths #

data_path = "donnéesDocteur\\"
pop_path = data_path+"Population\\"
geojson_repo_rul = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"

########################################################
###       Reading csv files containing the data      ###
########################################################

print("création des fichiers et du serveur dash veuillez patientez...")
print("le processus peut prendre une trentaine de seconde")

# age data #
medecin_age_csv = pd.read_csv(data_path+"Medecin_age_annee.csv")
infirmier_age_csv = pd.read_csv(data_path+"Infirmier_age_annee.csv")
dentiste_age_csv = pd.read_csv(data_path+"Dentiste_age_annee.csv")

# department data #
medecin_departement_csv = pd.read_csv(data_path+"Medecin_departement_annee.csv",encoding="WINDOWS-1252")
infirmier_departement_csv = pd.read_csv(data_path+"Infirmier_departement_annee.csv",encoding="WINDOWS-1252")
dentiste_departement_csv = pd.read_csv(data_path+"Dentiste_departement_annee.csv",encoding="WINDOWS-1252")

# parity data #
medecin_sexe_csv = pd.read_csv(data_path+"Medecin_sexe_annee.csv")
infirmier_sexe_csv = pd.read_csv(data_path+"Infirmier_sexe_annee.csv")
dentiste_sexe_csv = pd.read_csv(data_path+"Dentiste_sexe_annee.csv")

# french population data #
pop_departement_2020_csv = pd.read_csv(pop_path+"Pop_departement_2020.csv",encoding="WINDOWS-1252",sep=";")

########################################################
###         Constant variable for the program        ###
########################################################

# age interval yaken for the age data
age_intervalle_medecin=[[20,29],[30,34],[35,39],[40,44],[45,49],[50,54],[55,59],[60,64],[65,79]]
age_intervalle_infirmier=[[20,24],[25,29],[30,34],[35,39],[40,44],[45,49],[50,54],[55,59],[60,64],[65,79]]
age_intervalle_dentiste=[[20,24],[25,29],[30,34],[35,39],[40,44],[45,49],[50,54],[55,59],[60,64],[65,79]]

# years disponible for the data (only for age and sexe)
years=["2012","2013","2014","2015","2016","2017","2018","2019","2020"]

########################################################
###  data dictionaries for the dataset's functions   ###
########################################################

def InitValueDictAge(profession,age_intervalle,year_data):
    """
    variables: profession= people's profession in the data, 
    age_intervalle= the age interval used for the data
    year_data= the data for a single year
    return : a dict with the data to make a diagram about the age of peoples in the profession specified
    """
    # initializing variables for the function
    age_repart=[]
    prof_repart=[]
    # making the data for the dictionary
    for i in range(1,10):
        intervalle = age_intervalle[i-1]
        for j in range(0,int(year_data[i].replace(" ",""))):
            age = intervalle[1] - j%(intervalle[1]-intervalle[0]+1)
            age_repart.append(age)
            prof_repart.append(profession)
    return {"age":age_repart,"profession":prof_repart}


def InitValueDictDepartement(pop_data,data,year):
    """
    variables: pop_data= data about the population in France,
    data = data about the number of professional in each French departments,
    year = the year the data was taken
    return : a dict with the data to make a circulair diagram about parity
    """
    # initializing variables for the function 
    depart_pop_data= list(pop_data["Population par département"])
    val_pop_data= list(pop_data[pop_data.keys()[1]])
    depart_data= list(data[data.keys()[0]])
    year_data= list(data[year])
    depart=[]
    nom_depart=[]
    medecin_repart=[]
    # making the data for the dictionary
    for i in range(0,len(depart_pop_data)):
        if(type(depart_pop_data[i]) != type("bonjour")) : continue # if variables is not a string, continuing

        for j in range(0,len(depart_data)):
            if(type(depart_data[j]) != type("bonjour")) : continue # if variables is not a string, continuing

            # formating the two codes to compare them
            code_depart_pop = depart_pop_data[i][0:3].replace(" ","")
            code_depart = depart_data[j][0:3].replace(" ","")
            if(code_depart[0]=='0'): code_depart=code_depart[1:3]
            # checking if the two department are the same with their codes
            if(code_depart == code_depart_pop):
                # if true, creating the data 
                depart.append(code_depart)
                nom_depart.append(depart_data[j][depart_data[j].index("-")+1:])
                medecin_repart.append((float(val_pop_data[i].replace(" ","").replace(",","."))*1000) / float(year_data[j].replace(" ","").replace(",",".")))

    return {"departement":depart,"habitants par medecin":medecin_repart,"nom departement":nom_depart}
    

def InitValueDictSexe(profession,year_data):
    """
    variables : profession= people's profession in the data, year_data= the data for a single year
    return : a dict with the data to make a circular diagram about parity
    """
    return {"sexe":["Femme","Homme"],"count":[int(year_data[1].replace(" ","")), int(year_data[2].replace(" ",""))],
            "profession":[profession,profession]}


def AggregateDataDict(dict_list):
    """
    variables : a list of dict of the same format 
    aggregate all the data in the dictionaries together
    return : a dictionary with all the data
    """
    res_dict = dict_list[0]
    for i in range(1,len(dict_list)):
        for key in res_dict.keys():
            res_dict[key] = res_dict[key] + dict_list[i][key]
    return res_dict

########################################################
###     Creating all the DataFrame's functions       ###
########################################################

def CreateDataAge():
    """
    creates the data for the diagram for each years disponible
    return : a dictionary with all the data about age
    """
    medecin_age_data={}
    infirmier_age_data={}
    dentiste_age_data={}
    age_data={}

    for year in years:
        medecin_age_data[year] = InitValueDictAge("Médecin", age_intervalle_medecin,medecin_age_csv[year])
        infirmier_age_data[year] = InitValueDictAge("Infirmier", age_intervalle_medecin,infirmier_age_csv[year])
        dentiste_age_data[year] = InitValueDictAge("Dentiste", age_intervalle_medecin,dentiste_age_csv[year])
        age_data[year] = AggregateDataDict([medecin_age_data[year],infirmier_age_data[year],dentiste_age_data[year]])
    return age_data

def CreateDataSexe():
    """
    creates the data for the circular diagram for each years disponible
    return : a dictionary with all the data about gender
    """
    medecin_sexe_data={}
    infirmier_sexe_data={}
    dentiste_sexe_data={}

    for year in years:
        medecin_sexe_data[year]= InitValueDictSexe("Médecin",medecin_sexe_csv[year])
        infirmier_sexe_data[year]= InitValueDictSexe("Infirmier",infirmier_sexe_csv[year])
        dentiste_sexe_data[year]= InitValueDictSexe("Dentiste",dentiste_sexe_csv[year])
    return {"medecin" : medecin_sexe_data, "infirmier" : infirmier_sexe_data, "dentiste" : dentiste_sexe_data}

def CreateDataDepart():
    """
    creates the data for the map (only 2020)
    return : a dictionary with all the data about geographical repartition
    """
    return InitValueDictDepartement(pop_departement_2020_csv,medecin_departement_csv,"2020")

########################################################
###      Creating all the Figures' functions         ###
########################################################

def CreateHistogram(age_data):
    """
    value : dictionary containing all the data about age
    return : an histogram representing the values
    """
    histogramme_age={}
    for year in years:
        histogramme_age[year] = px.histogram(age_data[year],x="age",nbins=12,facet_col="profession",histnorm="probability",
                                         labels={"profession=":""},
                                         color_discrete_sequence=['indianred']
                                        ) 
        histogramme_age[year]["layout"]["yaxis_title"] = "probability"
    return histogramme_age

def CreatePie(sexe_data):
    """
    value : dictionary containing all the data about gender
    return : a circular histogram representing the values
    """
    pie_sexe_medecin={}
    pie_sexe_infirmier={}
    pie_sexe_dentiste={}

    for year in years:
        pie_sexe_medecin[year]= px.pie(sexe_data["medecin"][year],values="count",names="sexe",color_discrete_sequence=px.colors.sequential.RdBu)
        pie_sexe_infirmier[year]= px.pie(sexe_data["infirmier"][year],values="count",names="sexe",color_discrete_sequence=px.colors.sequential.RdBu)
        pie_sexe_dentiste[year]= px.pie(sexe_data["dentiste"][year],values="count",names="sexe",color_discrete_sequence=px.colors.sequential.RdBu)
    return {"medecin" : pie_sexe_medecin, "infirmier" : pie_sexe_infirmier, "dentiste" : pie_sexe_dentiste}

def CreateMap(map_data):
    """
    value : dictionary containing all the data about geographical repartition of doctors
    return : a map representing the values
    """
    geojson_departement_france = requests.get(geojson_repo_rul).json()

    map_repartition_medecin = px.choropleth(
                    map_data,
                    geojson=geojson_departement_france,
                    locations="departement",
                    featureidkey="properties.code",
                    color_continuous_scale="magma",
                    color="habitants par medecin",
                    scope="europe",
                    hover_data=["nom departement","departement","habitants par medecin"]
                    )
    map_repartition_medecin.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
    map_repartition_medecin["layout"]["height"] = 750
    return map_repartition_medecin


########################################################
###      Creating all the layouts for the app        ###
########################################################

# initializing data #
data = {
    "age"    : CreateDataAge(),
    "sexe"   : CreateDataSexe(),
    "depart" : CreateDataDepart()
}

# initializing figures #
histogramme_age = CreateHistogram(data["age"])

pie_sexe = CreatePie(data["sexe"])
pie_sexe_medecin = pie_sexe["medecin"]
pie_sexe_infirmier = pie_sexe["infirmier"]
pie_sexe_dentiste = pie_sexe["dentiste"]

map_repartition_medecin = CreateMap(data["depart"])

# default year #
year="2012"

# creating the dash app #
app = dash.Dash(__name__)

##### histogramme layout ######

histogramme_layout = [

                        html.H1(children=f'Age des travailleurs dans la profession de la médecine : ({year})',
                                style={'textAlign': 'center', 'color': '#7FDBFF'},
                                id="title_histogramme"),

                        dcc.Graph(
                            id='histogramme',
                            figure=histogramme_age["2012"]
                        ), 

                        html.Div(children=f'''
                                Cette histogramme représente la répartition des professionels de santé (médecin,dentiste,infirmier)
                                selon leurs ages
                            ''',
                                style={'textAlign': 'center'}), 

                        
                        html.Div(children=[
                            html.H2(children='Year'),
                            dcc.Slider(
                                id="slider_year_histogramme",
                                min=2012,
                                max=2020,
                                step=1,
                                value=2012,
                                updatemode="drag",
                                marks={
                                        2012: '2012',
                                        2013: '2013',
                                        2014: '2014',
                                        2015: '2015',
                                        2016: '2016',
                                        2017: '2017',
                                        2018: '2018',
                                        2019: '2019',
                                        2020: '2020'
                                    },
                                ),
                            ],
                            style={'textAlign': 'center','height': '50px', 'width': '50%','display': 'inline-block',"padding-left":"25%", "padding-right":"25%","padding-top":"25px"}
                        ), 

                    ]


##### histogramme functions ######

@app.callback(  
    [Output('histogramme','figure'),
    Output('title_histogramme','children')
    ],
    [Input('slider_year_histogramme', 'value')]
)
def update_histogramme(year):
    year=str(year)
    return [histogramme_age[year],f'Age des travailleurs dans la profession de la médecine : ({year})']


##### pie layout ######

pie_layout = [

                        html.H1(children=f'Age des travailleurs dans les professions de la médecine : ({year})',
                                style={'textAlign': 'center', 'color': '#7FDBFF'},
                                id="title_pie"),

                        html.Div(
                            dcc.Graph(
                                id='pie',
                                figure=pie_sexe_medecin["2012"]
                            ),
                            style={"width":"50%","padding-left":"25%", "padding-right":"25%"},
                        ),
                        

                        html.Div(children=f'''
                                Ce diagramme circulaire représente la proportion de femme et d'homme travaillant dans 
                                les professions de la médecine (médecin, infirmier et dentiste) entre 2012 et 2020.
                            ''',
                                style={'textAlign': 'center'}), 

                        html.Div(children=[
                            html.H2(children='Profession'),
                            dcc.Dropdown(
                            id="dropdown_profession_pie",
                            options=[
                                {'label': 'Medecin', 'value': "medecin"},
                                {'label': 'Infirmier', 'value': "infirmier"},
                                {'label': 'Dentiste', 'value': "dentiste"},
                                ],
                             value="medecin",
                                )
                            ],
                            style={'textAlign': 'center','height': '50px', 'width': '30%','display': 'inline-block',"padding-left":"35%", "padding-right":"35%","padding-top":"25px"}
                        ),
                        
                        html.Div(children=[
                            html.H2(children='Year'),

                            dcc.Slider(
                                id="slider_year_pie",
                                min=2012,
                                max=2020,
                                step=1,
                                value=2012,
                                updatemode="drag",
                                marks={
                                        2012: '2012',
                                        2013: '2013',
                                        2014: '2014',
                                        2015: '2015',
                                        2016: '2016',
                                        2017: '2017',
                                        2018: '2018',
                                        2019: '2019',
                                        2020: '2020'
                                    },
                                ),
                            ],
                            style={'textAlign': 'center','height': '80px', 'width': '50%','display': 'inline-block',"padding-left":"25%", "padding-right":"25%", "padding-top":"50px"}
                        ), 
]


##### pie functions ######

@app.callback(  
    [Output('pie','figure'),
    Output('title_pie','children')
    ],
    [Input('slider_year_pie', 'value'),
     Input('dropdown_profession_pie', 'value'),
    ]
)
def update_pie_year(year,profession):
    if(profession == "infirmier") : data = pie_sexe_infirmier
    elif(profession == "dentiste") : data = pie_sexe_dentiste
    else : data = pie_sexe_medecin
    year=str(year)
    return [data[year], f'Parité dans les professions de la médecine : ({year})']

##### map layout ######

map_layout = [
                        html.H1(children=f'Répartition des médecins sur le territoire Français : ({year})',
                                style={'textAlign': 'center', 'color': '#7FDBFF'},
                                id="title_map"),

                        html.Div(
                            dcc.Graph(
                                id='map_medecin',
                                figure=map_repartition_medecin
                            ),
                        ),

                        html.Div(children=f'''
                                Cette map représente la répartition des professionels de santé (médecin,dentiste,infirmier)
                                sur le territoire français, selon le nombre d'habitants par médecin dans chaque département.
                            ''',
                                style={'textAlign': 'center'}), 
]

##### general layout ######

general_layout = html.Div(children=[
                    dcc.Location(id='url', refresh=False),

                    html.Div(children=histogramme_layout,
                        id="page",
                        style={"padding-bottom":"75px"}
                    ),

                    html.Div(
                        children=[
                            dcc.Link(
                                html.Button('Histogramme'),
                                href='/Histogramme',
                                style={"margin-left":"35%"}),
                                dcc.Link(
                                html.Button('Pie'),
                                href='/Pie',
                                style={"margin-left":"9.2%"}),
                                dcc.Link(
                                html.Button('Map'),
                                href='/Map',
                                style={"margin-left":"10%"}),
                            ],
                        ),

                    dcc.Interval(   
                            id='interval',
                            interval=1*1000,
                            ),
                         
                    ]
)

##### general functions ######

@app.callback(dash.dependencies.Output('page', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if (pathname == "/Histogramme") : return histogramme_layout
    elif (pathname == "/Pie") : return pie_layout
    elif (pathname == "/Map") : return map_layout
    else : return histogramme_layout

if __name__ == "__main__":

    app.layout = general_layout
    app.run_server(debug=False)