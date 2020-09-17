import dash_core_components as dcc
import dash_html_components as html
import dash
import numpy as np
from modules import DashModul

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

_arr = np.random.normal(100, size=800)
DM = DashModul()
fig = DM.histPlot(_arr)

def get_layout():
    return html.Div(
        id="app-container",
        children=[
            # Banner
            html.Div(
                id="banner",
                className="banner",
                children=[html.Img(src=app.get_asset_url("uglylogo.png"))],
            ),
            html.Div(
                id="csv_loader",
                className="four columns",
                children=[
                    html.Div([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        )
                    ]
                    ),
                    html.Div(id='pos_right',
                             className="four columns",
                             children=[
                                 html.Div([
                                     dcc.Loading(id="loading", children=[html.Div([html.Div(id="t_status")])],
                                                 type="circle",
                                                 )
                                    ]
                                 ),
                             ]
                             ),
                    ]
            ),
            html.Div(
                id="left-column",
                className="four columns",
                children=[
                    html.Div(
                            id="description-card",
                            children=[
                                html.H5("Web Analytics"),
                                html.H3("Welcome to the WebPlots"),
                                html.Div(
                                    id="intro",
                                    children="Explore your data using advanced graphs and tabs",
                                        ),
                                html.Br(),
                                    ],
                            ),
                    html.Div(id="left-table",
                             className="twelve columns",
                             children=[
                                 html.Div(id='describe_table'),
                                 html.H5("Select filter columns"),
                                 dcc.Dropdown(id='dropdown_table_filterColumn',
                                              multi=True,
                                              placeholder='Filter Column'),
                                 html.H5("Select range column"),
                                 dcc.Dropdown(id='dropdown_table_rangeColumn',
                                              multi=False,
                                              placeholder='Range Column'),
                                 html.Br(),
                                 html.Div([
                                     dcc.RangeSlider(
                                         id='data-slider',
                                            ),
                                        ]
                                    ),
                                 html.H5("Or typing lower and upper values"),
                                 dcc.Input(id="input1", type="text", placeholder=""),
                                 dcc.Input(id="input2", type="text", placeholder=""),
                                 html.H5("Select a column for plots"),
                                 dcc.Dropdown(id='dropdown_table_plotColumn',
                                              multi=False,
                                              placeholder='Plot Column'),
                                ]
                             ),

                    html.Div(dcc.Input(id='session_code', type='text', style=dict(display='none'))),
                    html.Button('Load session', id='load-val', n_clicks=0, style=dict(display='none')),
                    #html.Div(id='load-button-basic', children='Load your configuration', style=dict(display='none')),

                    html.Button('Save session', id='submit-val', n_clicks=0),
                    html.Div(id='container-button-basic',
                            children='Enter a value and press submit')
                    ]
            ),
            # Right column]),
            html.Div(
                id="right-column",
                className="eight columns",
                children=[
                    html.Div(
                        id="graph_pad",
                        children=[
                            #html.B("Patient Volume"),
                            html.Hr(),
                            dcc.Graph(id='tabs-example-content', figure=fig)
                        ],
                    ),
                    html.Div(dcc.Tabs(id='tabs-example', value='HeatMap', children=[
                                dcc.Tab(label='HeatMap', value='HeatMap'),
                                dcc.Tab(label='HistPlot', value='HistPlot'),
                                dcc.Tab(label='boxPlot', value='boxPlot'),
                                dcc.Tab(label='distPlot', value='distPlot'),
                        ])),
                    html.Div(id='Table_'),
                    ],
                ),
            html.Div(id='settings_table')
            ])