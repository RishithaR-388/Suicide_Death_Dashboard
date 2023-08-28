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
years = df["Year"].unique()

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
            className="gap1"
        ),
        html.Div(
            html.Div(
                dcc.Dropdown(
                        id = "select_year",
                        options = [
                            {"label":year,"value" : year} for year in years
                        ],
                        multi = False,
                        value = years[5], 
                        style = {"height":"40px","width":"350px","border-radius":"45px","text":"bold"}, 
                        # style = {"border-radius":"45px","height":"20px","width":"350px", "text":"bold","background-color":"grey"},
                        className= "dcc_comp"
                    ),
                className="year_comp"
                ),
            className = "year_select"
        ),
        html.Div(
            className="gap1"
        ),
        html.Div(
            dcc.Graph(
                id='map', 
                figure={},
            ),
            className="graph"   
        )
    ]
)
      
@callback(
    Output(component_id='map', component_property='figure'),
    # Output(component_id='graph', component_property='figure'),
    [
    Input(component_id='select_year', component_property='value')
    ]
    
)       


def update_graph(year_selected):
    
    
    # container = "The year chosen by user was: {}".format(year)
    df1 = df.copy()
    df2 = df1[df1["Year"] == year_selected]
    df3 = df2[["Country","Suicides100kPop","Population","GdpPerCapitalMoney"]]
    df3 = df3.groupby("Country").sum()
    df3 = df3.reset_index()

    fig = px.choropleth(
            df3,
            locationmode = 'country names',
            locations = df3["Country"], 
            color = "Suicides100kPop", 
            hover_data = ["Suicides100kPop","Population","GdpPerCapitalMoney"],
            projection = 'natural earth',
            width = 1200,
            height = 800,
            hover_name = "Country",
            title = "Suicides in year :- " + str(year_selected),
            color_continuous_scale = px.colors.sequential.Blues,
        )
    fig.update_layout(
        title_font_color = "black",
        title_font_family = "PT Sans Narrow",
        title_x = 0.45,
        title_font_size = 30,
        paper_bgcolor = "#5C8374",
        margin_b = 100,
        font_family = "Times New Roman",
        font_color = "black",
        font_size = 15

    )

    return fig