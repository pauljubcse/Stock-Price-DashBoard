import dash
from dash import dcc
from dash import html 
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output, State
import yfinance as yf
import dash_auth
from datetime import datetime
import pandas as pd

app = dash.Dash()
AUTH=[['apaul', 'apauldash']]
auth =dash_auth.BasicAuth(app, AUTH)
server=app.server

nsdq=pd.read_csv('nasdaq_screener_1683452962816.csv')
nsdq.set_index('Symbol', inplace=True)
options=[]
nsdq.head(5)
for tk in nsdq.index:
    try:
        tick=str(tk)
        options.append({'label': nsdq.loc[tick]['Name']+' '+tick, 'value': tick})
    except:
        continue
    
app.layout = html.Div([
    #html.Div('Dash: Web Dashboards with Python', style={'textAlign':'center', 'color':colors['text']}),
    html.Div([
        html.H1('Stock Ticker Dashboard with Python', style={'textAlign':'center', 'color':'#9BA4B5','font-family' : "'Roboto', sans-serif"}),
        html.P(),
        html.Div([
            html.Div([
                html.H3('Enter Stock Symbol', style={
                                                    'textAlign':'center',
                                                    'color':'#9BA4B5',
                                                    'font-family' : "'Roboto', sans-serif"
                                                    }),
                html.P(),
                dcc.Dropdown(
                    id='symbol-select',
                    options=options,
                    value=['TSLA'],
                    multi=True
                )
            ], style={
                
            }),
            
        ]),

        html.Div([
            html.Div([
                html.H3('Enter Date Range', style={'textAlign':'center', 'color':'#9BA4B5','font-family' : "'Roboto', sans-serif"}),
                dcc.DatePickerRange(id='date-input',
                                    min_date_allowed=datetime(2015,1,1),
                                    max_date_allowed=datetime.today(),
                                    start_date=datetime(2018,1,1),
                                    end_date=datetime.today(),
                                    style={
                                        
                                        }),
            ], style={

            }),
            html.Div([
                html.Button(id='submit-button', n_clicks=0, children='Submit',
                        style={
                            'font-family' : "'Roboto', sans-serif",
                            'width':'120px',
                            'height':'50px',
                            'border-radius':'10px',
                        })
            ], style={'paddingTop':'55px'})

        ], style = {
            'display' :'flex',
            'flex-direction' : 'row',
            'justify-content' : 'space-around'
        }),
        
        
        html.P(),

        dcc.Graph(id='stock-graph', figure={'data':[go.Scatter(x=[1,2,3], y=[1,2,3], mode='lines' )],
                                            'layout': go.Layout(title='TITLE',template='plotly_dark')}),
    ], id='main',
    style={
        'background-color':'#000000',
        'padding': '10px',
        'border-radius' : '5px',
        'box-shadow' : '0 0 150px 30px #000000',
        'display':'flex',
        'flex-direction':'column'
        },
    )
])

@app.callback(
        Output('stock-graph','figure'),
        [Input('submit-button', 'n_clicks')],
        [State('symbol-select','value'),
        State('date-input','start_date'),
        State('date-input','end_date')],
    )

def update_graph(n_clicks, stock_ticker, start_date, end_date):
    print('______________________________________________________')
    print(stock_ticker)
    start=datetime.strptime(start_date[:10], '%Y-%m-%d')
    end=datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces=[]
    for tic in stock_ticker:
        df=yf.download(tic, start, end)
        traces.append({'x': df.index, 'y':df['Close'].values, 'name':tic})
    
    fig={'data':traces,
        'layout': go.Layout(title='Prices', template='plotly_dark')
    }
    return fig

if __name__=='__main__':
    app.run_server()