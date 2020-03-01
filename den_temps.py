import dash
import dash_html_components as html
import dash_core_components as dcc
# from connect import norm_records, rec_lows, rec_highs, all_temps
from datetime import datetime, date, timedelta
import time
# from connect import all_temps
import pandas as pd

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

current_year = datetime.now().year
today = time.strftime("%Y-%m-%d")
startyr = 1950
year_count = current_year-startyr



df_norms = pd.read_csv('normals.csv')


df_all_temps = pd.read_csv('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN&stations=USW00023062&startDate=1950-01-01&endDate=2020-02-26&units=standard')

df_all_temps['DATE'] = pd.to_datetime(df_all_temps['DATE'])
df_all_temps = df_all_temps.set_index('DATE')

daily_highs = df_all_temps.resample('D').max()
df_rec_highs = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).max()

high_idx = df_rec_highs.index.get_level_values(0).astype(str) + '-' + df_rec_highs.index.get_level_values(1).astype(str)
df_rec_highs.index = high_idx

last_day = df_all_temps.index[-1]
ld = last_day.strftime("%Y-%m-%d")


daily_lows = df_all_temps.resample('D').min()
df_rec_lows = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).min()
low_idx = df_rec_lows.index.get_level_values(0).astype(str) + '-' + df_rec_lows.index.get_level_values(1).astype(str)
df_rec_lows.index = low_idx


def temp_App():
    return html.Div(
        [
            html.Div([
                html.Div([
                        html.Div([
                            dcc.Link('Home', href='/'),
                        ],
                            className='one column'
                        ),
                        html.Div([
                            dcc.Link('Arctic Ice', href='/ice'),
                        ],
                            className='two columns'
                        ),
                        html.Div([
                            dcc.Link('Colorado River', href='/colorado-river'),
                        ],
                            className='two columns'
                        ),
                        html.Div([
                            dcc.Link('CO2', href='/co2'),
                        ],
                            className='two columns'
                        ),
                    ],
                    className='twelve columns'
                    ),
          ],
            className='row'
          ),
            html.Div([
                html.H2(
                    'Denver Temperature Record',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    'NOAA Stapleton Station Data',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                  '1950-01-01 through {}'.format(ld),
                  className='twelve columns',
                  style={'text-align': 'center'})
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Label('Select Product', style={'text-align': 'center'}),
                    html.Div([
                        dcc.RadioItems(
                        id='product',
                        options=[
                            {'label':'Temperature graphs', 'value':'temp-graph'},
                            {'label':'Climatology for a day', 'value':'climate-for-day'},
                            {'label':'Full Record Bar Graphs', 'value':'frbg'},
                            {'label':'5 Year Moving Avgs', 'value':'fyma-graph'},
                            {'label':'Full Record Heat Map', 'value':'frhm'},
                        ],
                        # value='temp-graph',
                        labelStyle={'display': 'block'},
                        ),
                    ],
                        className='pretty_container'
                    ),   
                ],
                    className='three columns',
                ),
                html.Div([
                    html.Div(
                        id='year-picker'
                    ),
                    html.Div(
                        id='date-picker'
                    ),
                ],
                    className='four columns',
                ),
                # html.Div([
                #     html.Button('Update Data', id='data-button'),
                # ]),
                html.Div([
                    html.Div(id='output-data')
                ]),

            ],
                className='row'
            ),
            html.Div([
                html.Div(
                    [
                        html.Div(id='period-picker'),
                    ],
                ),
    
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='graph'
                    ),
                ],
                    className='eight columns'
                ),
                html.Div([
                    dcc.Loading(
                        id='loading-1',
                        children=[
                            html.Div([
                                html.Div(id='graph-stats'
                                ),
                            ],
                            ),
                            html.Div([
                                html.Div(id='fyma-stats'
                                ),
                            ],
                            ),
                        ]
                    ),
                    html.Div([
                        html.Div(id='frs-bar-controls'
                        ),
                    ],
                    ),
                    html.Div([
                        html.Div(id='frs-heat-controls'
                        ),
                    ],
                    ),
                    
                ],
                    className='four columns'
                ),    
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='climate-day-table'
                    ),
                ],
                    className='five columns'
                ),
                html.Div([
                    html.Div([
                        html.Div(
                            id='bar'
                        ),
                    ],
                        className='twelve columns'
                    ),
                ],
                    className='seven columns'
                ),     
            ],
                className='row'
            ),
            html.Div([
              html.Div([
                html.Div([
                  html.Div(id='daily-stats'),
                ]),
              ],
                className='twelve columns'
              ),
            ],
                className='row'
            ),
            
            html.Div(id='all-data', style={'display': 'none'}),
            html.Div(id='rec-highs', style={'display': 'none'}),
            html.Div(id='rec-lows', style={'display': 'none'}),
            html.Div(id='norms', style={'display': 'none'}),
            html.Div(id='temp-data', style={'display': 'none'}),
            html.Div(id='df5', style={'display': 'none'}),
            html.Div(id='max-trend', style={'display': 'none'}),
            html.Div(id='min-trend', style={'display': 'none'}),
            html.Div(id='d-max-max', style={'display': 'none'}),
            html.Div(id='avg-of-dly-highs', style={'display': 'none'}),
            html.Div(id='d-min-max', style={'display': 'none'}),
            html.Div(id='d-min-min', style={'display': 'none'}),
            html.Div(id='avg-of-dly-lows', style={'display': 'none'}),
            html.Div(id='d-max-min', style={'display': 'none'}),
            html.Div(id='temps', style={'display': 'none'}),
        ]
    )

app.layout = temp_App