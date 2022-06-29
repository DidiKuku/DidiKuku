import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('games.csv')

#предобработка
df = df.drop(['Name', 'Critic_Score', 'User_Score', 'Rating'], axis = 1)
df.dropna(subset = ['Year_of_Release'], inplace = True)
df.dropna(subset = ['Genre'], inplace = True)
df['all_sales'] = df['NA_sales'] + df['EU_sales'] + df['JP_sales'] + df['Other_sales']
all_platform = df['Platform'].unique()

app.layout = html.Div([

    html.H1("Sales in different years", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2012", "value": 2012},
                     {"label": "2013", "value": 2013},
                     {"label": "2014", "value": 2014},
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     ],
                 multi=False,
                 value=2012,
                 style={'width': "40%"}
                 ),

    
    dcc.Dropdown(id="slct_platform",
        options=[{'label': i, 'value': i} for i in all_platform],
                value='Wii',
                style={'margin-top': '20px', 
                       'width': "40%"
                }  
    ),

    dcc.Graph(id='genres', figure={}),

    #dcc.Graph(id='boxplot', figure={})

])

@app.callback(
     Output('genres', 'figure'),
    [Input('slct_year', 'value'),
    Input('slct_platform', 'value')]
)
def update_graph(slctd_year, slct_platform):
    print(slctd_year, slct_platform)

    dff = df.copy()
    dff = dff[dff["Year_of_Release"] == slctd_year]
    dff=dff[dff['Platform'] == slct_platform]

    fig = px.bar(dff, x="Genre", y="all_sales")
    return fig

"""@app.callback(
    Output('boxplot', 'figure'),
    [Input('slct_year', 'value'),
    Input('slct_platform', 'value')]
def update_boxplot(year, platform):
    print(f"hoverData: {hoverData}")
    dff = df.copy()
    dff = dff[dff["Year_of_Release"] == year]
    dff=dff[dff['Platform'] == platform]
    fig = px.box(dff, x='Platform', y='all_sales')
    return fig"""
    

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
