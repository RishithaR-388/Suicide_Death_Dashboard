import pandas as pd
import numpy as np
import math
import plotly.express as px  
import dash
from dash import dcc,html,callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd




df = pd.read_csv("data/Sucide_Deaths.csv")
countries = df["Country"].unique()

app = dash.Dash(__name__, suppress_callback_exceptions=True)

layout = html.Div(
    children = [
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.H1('Suicide Deaths Dashboard',className="heading"),
                        html.H5('From 1987-2016',className="sub-heading"),
                    ],
                    className = "title1"
                ),
                html.Div(
                    children = [
                        html.Div(
                            dcc.Link('Charts', href='/page',className="pageitem"), className="pagelink"
                        ),
                        html.Div(
                            dcc.Link('Maps', href='/page1',className="pageitem"), className="pagelink"
                        ),
                    ],
                    className = "title2"
                ),
            ],
            className = "title_panel"
        ),
        html.Div(
        children = [
            html.Div(
                children = [
                    # left side column for inputs
                    html.Div(
                        html.Div(
                            children = [
                                # for 1st dropbox ----- country
                                html.Div(
                                    dcc.Dropdown(
                                        id = "select_country",
                                        options = [
                                            {"label":country,"value" : country} for country in countries
                                        ],
                                        style = {"padding-right":"3%","border-radius":"45px"},
                                        multi = False,
                                        value = countries[5],  
                                        className= "dcc_comp"
                                    ),
                                className="country_dropdown"
                                ),
                                # for 2nd dropbox ---- sex/age/Generation
                                html.Div(
                                    dcc.Dropdown(
                                        id = "select_type",
                                        options = [ 
                                            "Sex","Generation","Age"
                                        ],
                                        style = {"padding-right":"3%","border-radius":"45px"},
                                        multi = False,
                                        value = "Sex",
                                        className= "dcc_comp"
                                    ),
                                className="type_dropdown"
                                ),
                            ],
                            className = "subcol1"
                        ),
                        className = "col1"
                    ),
                    # right side column for outputs
                    html.Div(
                        html.Div(
                            children = [
                                html.Div(
                                    id = "Select Graph Title",
                                    className = "graph_title"
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id='graph', 
                                        figure={},
                                        style={ 'border-radius':'45px','background-color':'white'},
                                        className = "chart"
                                    )
                                )
                            ],
                            className = "subcol2"
                        ),
                        className = "col2"
                    )
                ],
                className = "row"
            ),
            html.Div(
                className="gap3"
            ),
            # For Country-Suicide Map
            html.Div(
                html.Div(
                    children = [
                        # html.Div(
                        #     html.H3("Sucides Per 100k population Over the Years For the Country",
                        #     className = "chart_heading"
                        #     )
                        # ),
                        dcc.Graph(
                            id = "line_chart1",
                            figure={},
                            className="line_body"
                        )
                    ],
                    className = "country_map"
                ),
                className = "line_bg"
            ),
            html.Div(
                className="gap2"
            ),
            # for Country-GDP map
            html.Div(
                html.Div(
                    children = [
                        # html.Div(
                        #     html.H3("GDP Per Capita Over the Years For the Country",className = "chart_heading")
                        # ),
                        dcc.Graph(
                            id = "line_chart2",
                            figure={},
                            className="line_body"
                        )
                    ],
                    className = "country_map"
                ),
                className = "line_bg"
            ), 
        ],
        className = "body_bg" )
    ]
)
            
      
      
@callback(
    [Output(component_id='line_chart2', component_property='figure'),
        Output(component_id='line_chart1', component_property='figure')],
    Output(component_id='graph', component_property='figure'),
    [
    Input(component_id='select_country', component_property='value'),
    Input(component_id='select_type', component_property='value')
    ]
    
)       


def update_graph(country,type):
    
    
    # container = "The year chosen by user was: {}".format(year)
    df1 = df.copy()
    df2 = df1[df1["Country"] == country]

    ## for fig1
    df_ = df2[["Country","Year","Suicides100kPop"]]
    df_ = df_.groupby(["Country",'Year'])['Suicides100kPop'].sum()
    df_ = df_.reset_index()

    ## for fig2
    df__ = df2[["Country","Year","GdpPerCapitalMoney"]]
    df__ = df__.groupby(["Country",'Year'])['GdpPerCapitalMoney'].sum()
    df__ = df__.reset_index()

    # plotly express for line graphs for selected country

    # Year to Suicide for a country
    fig1 = px.line(
        df_, 
        x = df_["Year"],
        y = df_["Suicides100kPop"], 
        color="Country",
        width = 1200,
        height= 800,
        title="Suicides Per 100k population Over the Years For the Country"
    )

    fig1.update_layout(
        title_font_color = "black",
        title_font_family = "PT Sans Narrow",
        title_x = 0.7,
        title_font_size = 30,
        paper_bgcolor = "#5C8374",
        margin_b = 100,
        font_family = "Times New Roman",
        font_color = "black",
        font_size = 15,
        # plot_bgcolor = "brown" 

    )
    # Year to GDP for a country

    fig2 = px.line(
        df__, 
        x = df__["Year"],
        y = df__["GdpPerCapitalMoney"], 
        color="Country",
        width = 1200,
        height= 800,
        title="GDP Per Capita Over the Years For the Country"
    )

    fig2.update_layout(
        title_font_color = "black",
        title_font_family = "PT Sans Narrow",
        title_x = 0.7,
        title_font_size = 30,
        paper_bgcolor = "#3c5d51",
        margin_b = 100,
        font_family = "Times New Roman",
        font_color = "black",

        # plot_bgcolor = "brown" ,
        font_size = 15
    )
    # fig2.update_layout(
    #     title_font_color = "black",
    #     title_font_family = "PT Sans Narrow",
    #     title_font_size = 30,
    #     paper_bgcolor = "#D46B37",

    # )


    fig3 = None
    ## for sex pie chart
    df3 = df2.copy()
    if type == "Sex":
        df3 = df3[['Gender', 'Suicides100kPop']]
        df3 = df3.groupby('Gender')['Suicides100kPop'].sum()
        df3 = df3.reset_index()
        fig3 = px.pie(df3, values='Suicides100kPop', names='Gender',title="Gender Vs Suicides")

    # for Generation Graph
    if type == "Generation":
        df3 = df3[['Generation', 'Suicides100kPop']]
        df3 = df3.groupby('Generation')['Suicides100kPop'].sum()
        df3 = df3.reset_index()
        fig3 = px.bar(df3, x='Generation', y='Suicides100kPop',color="Generation",title="Generation Vs Suicides")
    
    # for Age Graph
    elif type == "Age":
        df3 = df3[['Age', 'Suicides100kPop']]
        df3 = df3.groupby('Age')['Suicides100kPop'].sum()
        df3 = df3.reset_index()
        fig3 = px.pie(df3, values='Suicides100kPop', names='Age',title="Age Vs Suicides")
    

    fig3.update_layout(
        title_font_color = "black",
        title_font_family = "PT Sans Narrow",
        title_x = 0.5,
        title_font_size = 20,
        paper_bgcolor = "#5C8374",
        # margin_b = 100,
        # height = 240,
        # width = 750,
        font_family = "Times New Roman",
        font_color = "black",
        font_size = 15

    )
    # fig3.update_layout(
    #     paper_bgcolor = "#37D472"
    # )

    return fig2,fig1,fig3




