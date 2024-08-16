import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
from threading import Timer

# Load the dataset
file_path = 'Players_data_23-24.csv'  # Update with your file path
players_data = pd.read_csv(file_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate the cost marks for the slider at 0.5 increments
cost_min = 4  # Starting point
cost_max = players_data['now_cost'].max()
cost_marks = {i: {'label': f'{i:.1f}', 'style': {'color': '#7f7f7f'}} for i in range(int(cost_min * 2), int(cost_max * 2) + 1, 1)}  # Adjust to 0.5 steps

# Layout of the app
app.layout = html.Div(style={'font-family': 'Arial', 'margin': '20px'}, children=[
    html.H1("FPL Dashboard 2023-2024", style={'text-align': 'center', 'color': '#2C3E50'}),

    html.Div([
        html.Label("Filter by Position:"),
        dcc.Dropdown(
            id='position-filter',
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Goalkeeper', 'value': 'Goalkeeper'},
                {'label': 'Defender', 'value': 'Defender'},
                {'label': 'Midfielder', 'value': 'Midfielder'},
                {'label': 'Forward', 'value': 'Forward'}
            ],
            value='All'
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Cost Range:"),
        dcc.RangeSlider(
            id='cost-filter',
            min=cost_min,
            max=cost_max,
            step=0.5,  # Set step to 0.5
            marks={i: {'label': f'{i:.1f}', 'style': {'color': '#7f7f7f'}} for i in range(int(cost_min * 2), int(cost_max * 2) + 1, 1)},
            value=[cost_min, cost_max],
            tooltip={"placement": "bottom", "always_visible": True}  # Tooltip always visible
        ),
    ], style={'width': '60%', 'display': 'inline-block', 'padding': '0px 20px'}),

    html.Div([
        html.Label("Minimum Minutes Played:"),
        dcc.Slider(
            id='minutes-filter',
            min=0,
            max=int(players_data['minutes'].max()),
            step=10,
            marks={0: '0', 500: '500', 1000: '1000', 1500: '1500', 2000: '2000'},
            value=0
        ),
    ], style={'width': '100%', 'padding': '20px 0'}),

    dcc.Tabs([

        dcc.Tab(label='Top Performers', children=[
            dcc.Graph(id='top-performers')
        ]),

        dcc.Tab(label='Cost-Effective Players', children=[
            dcc.Graph(id='cost-effective-players')
        ]),

        dcc.Tab(label='Expected Goals vs Goals Scored', children=[
            dcc.Graph(id='expected-goals-vs-goals-scored')
        ]),
        
        dcc.Tab(label='Points per 90 Minutes', children=[
            dcc.Graph(id='points-per-90')
        ]),
        
    ])
])

# Define the cost_efficiency function
def cost_efficiency(df):
    df['value_for_money'] = df['total_points'] / df['now_cost']
    sorted_df = df[['first_name', 'second_name', 'total_points', 'now_cost', 'value_for_money']].sort_values(by='value_for_money', ascending=False)
    return sorted_df

# Define the plot_cost_efficiency function
def plot_cost_efficiency(df, min_cost=0):
    cost_efficiency_data = cost_efficiency(df)
    cost_efficiency_data = cost_efficiency_data[cost_efficiency_data['now_cost'] >= min_cost]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cost_efficiency_data['now_cost'],
        y=cost_efficiency_data['total_points'],
        mode='markers',
        marker=dict(
            size=10,
            color=cost_efficiency_data['value_for_money'],  # Color by value for money
            colorscale='Viridis',  # Apply a color scale
            colorbar=dict(title='Value for Money')  # Color bar to show scale
        ),
        text=cost_efficiency_data['first_name'] + ' ' + cost_efficiency_data['second_name'],  # Hover text
        hoverinfo='text+x+y'
    ))

    fig.update_layout(
        title='Total Points vs. Cost for Players',
        xaxis_title='Now Cost',
        yaxis_title='Total Points',
        template='plotly_white',  # Clean background for better visibility
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    
    return fig

# Callback for updating top performers graph
@app.callback(
    Output('top-performers', 'figure'),
    [Input('position-filter', 'value'),
     Input('cost-filter', 'value'),
     Input('minutes-filter', 'value')]
)
def update_top_performers(selected_position, selected_cost, min_minutes):
    filtered_data = players_data.copy()
    
    if selected_position != 'All':
        filtered_data = filtered_data[filtered_data['singular_name'] == selected_position]
    
    filtered_data = filtered_data[(filtered_data['now_cost'] >= selected_cost[0]) & 
                                  (filtered_data['now_cost'] <= selected_cost[1]) &
                                  (filtered_data['minutes'] >= min_minutes)]

    top_performers = filtered_data.nlargest(10, 'total_points')
    fig = px.bar(top_performers, x='web_name', y='total_points', 
                 title="Top Performers (Total Points)", 
                 labels={'web_name': 'Player', 'total_points': 'Total Points'},
                 color='total_points', color_continuous_scale='Viridis')

    return fig

# Callback for updating cost-effective players graph
@app.callback(
    Output('cost-effective-players', 'figure'),
    [Input('position-filter', 'value'),
     Input('cost-filter', 'value'),
     Input('minutes-filter', 'value')]
)
def update_cost_effective_players(selected_position, selected_cost, min_minutes):
    filtered_data = players_data.copy()
    
    if selected_position != 'All':
        filtered_data = filtered_data[filtered_data['singular_name'] == selected_position]
    
    filtered_data = filtered_data[(filtered_data['now_cost'] >= selected_cost[0]) & 
                                  (filtered_data['now_cost'] <= selected_cost[1]) &
                                  (filtered_data['minutes'] >= min_minutes)]

    fig = plot_cost_efficiency(filtered_data, min_cost=selected_cost[0])

    return fig

# Callback for updating expected goals vs goals scored graph
@app.callback(
    Output('expected-goals-vs-goals-scored', 'figure'),
    [Input('position-filter', 'value'),
     Input('cost-filter', 'value'),
     Input('minutes-filter', 'value')]
)
def update_expected_goals_vs_goals_scored(selected_position, selected_cost, min_minutes):
    filtered_data = players_data.copy()
    
    if selected_position != 'All':
        filtered_data = filtered_data[filtered_data['singular_name'] == selected_position]
    
    filtered_data = filtered_data[(filtered_data['now_cost'] >= selected_cost[0]) & 
                                  (filtered_data['now_cost'] <= selected_cost[1]) &
                                  (filtered_data['minutes'] >= min_minutes)]
    
    fig = px.scatter(filtered_data, x='expected_goals', y='goals_scored',
                     title="Expected Goals vs Goals Scored",
                     labels={'expected_goals': 'Expected Goals', 'goals_scored': 'Goals Scored'},
                     color='goals_scored', color_continuous_scale='Viridis',
                     hover_name='web_name')

    return fig

# Callback for updating points per 90 minutes graph
@app.callback(
    Output('points-per-90', 'figure'),
    [Input('position-filter', 'value'),
     Input('cost-filter', 'value'),
     Input('minutes-filter', 'value')]
)
def update_points_per_90_minutes(selected_position, selected_cost, min_minutes):
    filtered_data = players_data.copy()
    
    if selected_position != 'All':
        filtered_data = filtered_data[filtered_data['singular_name'] == selected_position]
    
    filtered_data = filtered_data[(filtered_data['now_cost'] >= selected_cost[0]) & 
                                  (filtered_data['now_cost'] <= selected_cost[1]) &
                                  (filtered_data['minutes'] >= min_minutes)]

    filtered_data['points_per_90'] = (filtered_data['total_points'] / filtered_data['minutes']) * 90

    fig = px.scatter(filtered_data, x='minutes', y='points_per_90',
                     title="Points per 90 Minutes",
                     labels={'minutes': 'Minutes Played', 'points_per_90': 'Points per 90 Minutes'},
                     color='points_per_90', color_continuous_scale='Viridis',
                     hover_name='web_name')

    return fig

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8051/")  # Updated port number

# Run the app and open in browser
if __name__ == '__main__':
    Timer(1, open_browser).start()  # Open browser after 1 second
    app.run_server(debug=True, port=8051)  # Change the port number to 8051
