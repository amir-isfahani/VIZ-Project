import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
# from world_population import get_population2022_fig
# from hepatitis_viz import get_hepatitis_fig
from olympic_history import get_olympic_history

# import hepatitis DataSet and drow a scatter 3D
hepatitis_df= pd.read_csv("F:\Hepatitis\Hepatitis_Viz\hepatitis.csv")
hepatitis_df.ffill(inplace=True)

hepatitis_df.drop_duplicates()
hepatitis_fig = px.scatter_3d(  hepatitis_df[['protime','albumin','bilirubin','class']],
                                x='protime',
                                y='albumin',
                                z='bilirubin',
                                color='class', title='Interactive 3D Scatter Plot of Iris Dataset',
                                labels={'class': 'alive'})
hepatitis_fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

# import world population DataSet and drow a treemap

# import world population DataSet and drow a treemap
olympic_df = pd.read_csv(r"F:\Hepatitis\Hepatitis_Viz\Olympic.csv")
olympic_df = olympic_df[olympic_df['Team'] == 'United States']
olympic_df.sort_values(by='Year', inplace=True, ascending=False)
olympic_df = olympic_df[olympic_df['Medal'].notna()]
medals_count = olympic_df.groupby(['Year', 'Medal']).size().unstack(fill_value=0)
medals_count['Dominant Medal'] = medals_count.idxmax(axis=1)
color_map = {'Gold': 'yellow', 'Silver': 'silver', 'Bronze': 'lightcoral'}
medals_count['Color'] = medals_count['Dominant Medal'].map(color_map)
medals_per_year = medals_count.reset_index()
olympic_fig = px.scatter(medals_per_year,
                x='Year',
                y=medals_per_year['Gold']+medals_per_year['Silver']+medals_per_year['Bronze'],
                size='Gold',
                title='Medals Won by United States per Year',
                labels={'y': 'Number of Medals', 'Year': 'Year'},
                color=medals_count['Color'],
                )
population_df = pd.read_csv('https://raw.githubusercontent.com/AlexTheAnalyst/PandasYouTubeSeries/main/world_population.csv')

population_df.ffill(inplace=True)

population_df.drop_duplicates(inplace=True)
treemap_fig = px.treemap(population_df,
                        path=[px.Constant("World Population"),"Continent","Country"],
                        values="2022 Population",
                        color_continuous_scale="Bluse",
                        title="WideWorld Population 2022",
                        
                        )
treemap_fig.update_traces(
    texttemplate='%{label}<br>%{value:,.0f}',
    textposition='middle center',
    hovertemplate='Population: <br>%{value:,.0f}',
)
app = Dash(__name__)
app.title = "Data Viz"
app.layout = html.Div([
    html.H1("Made by Amir Isfahani", style={"textAlign": "center"}),
    html.Br(),
    html.H2("1. Scatter 3D (Hepatitis dataset)"),
    dcc.Graph(figure=hepatitis_fig, config={'displayModeBar': False}),
    html.Br(),
    html.H2("2. Treemap (World Population 2022 dataset)"),
    dcc.Graph(figure=treemap_fig, config={'displayModeBar': False}),
    html.Br(),
    html.H2("3. Scatter Bouble(Olympic dataset)"),
    dcc.Graph(figure=olympic_fig, config={'displayModeBar': False}),
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
