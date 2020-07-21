import base64
import datetime
import io
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
from dash.dependencies import Input, Output, State
import dash_table_experiments as dte
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

from modules import DashModul

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

ref_df = pd.read_csv('/home/jager/Projects/kaggle/data/competitive-data-science-predict-future-sales/sales_train.csv')
col_unique_cnt = {}
for col in ref_df.columns:
    if ref_df[col].unique().shape[0] != ref_df.shape[0]:
        col_unique_cnt[ref_df[col].unique().shape[0]] = col
max_var_col = col_unique_cnt[max(col_unique_cnt)]

DM = DashModul()
fig = DM.histPlot(ref_df, max_var_col)

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
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
                    )]
        ),
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                html.Div(
                        id="description-card",
                        children=[
                            html.H5("Web Analytics"),
                            html.H3("Welcome to the Web Analytics Dashboard"),
                            html.Div(
                                id="intro",
                                children="Explore your data using advanced graphs and tabs",
                            ),
                            html.Br(),
                            # html.Button(
                            #     id='propagate-button',
                            #     n_clicks=0,
                            #     children='Propagate Table Data'
                            #),
                        ],
                    ),
                html.Div([
                    dcc.Graph(id='Mygraph1', figure=fig),
                    # html.Button('Submit', id='submit-val', n_clicks=0),
                    #dcc.Graph(id='Mygraph_1')
                    #html.Br(),
                    ]
                ),
                html.Div(id="control-card",
                        className="eight columns",
                        children=[
                        html.H5("Filter Column"),
                            dcc.Dropdown(id='dropdown_table_filterColumn',
                            multi=True,
                            placeholder='Filter Column'),
                        ]
                ),
            ]
        ),
        # Right column]),
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Patient Volume"),
                        html.Hr(),
                        dcc.Graph(id='Mygraph', figure=fig),
                    ],
                ),
                # Patient Volume Heatmap
                html.Div([
                    # html.Button('Submit', id='submit-val', n_clicks=0),
                    html.Div(id='Table_'),
                    #dcc.Graph(id='Mygraph_')
                    #html.H5("Updated Table"),
                    #html.Div(dte.DataTable(rows=[{}], id='table'))
                    ]
                ),
            ],
        ),
    ],
)

@app.callback(Output('dropdown_table_filterColumn', 'options'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
    return [{'label': i, 'value': i} for i in df.columns]

@app.callback(Output('Mygraph1', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        col_unique_cnt = {}
        for col in df.columns:
            if df[col].unique().shape[0] != df.shape[0]:
                col_unique_cnt[df[col].unique().shape[0]] = col
        max_var_col = col_unique_cnt[max(col_unique_cnt)]

        fig = DM.histPlot(df, max_var_col)

    return fig

@app.callback(Output('Mygraph_1', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        col_unique_cnt = {}
        for col in df.columns:
            if df[col].unique().shape[0] != df.shape[0]:
                col_unique_cnt[df[col].unique().shape[0]] = col
        max_var_col = col_unique_cnt[max(col_unique_cnt)]

        fig = DM.heatmapPlot(df, max_var_col)

    return fig

@app.callback(Output('Mygraph', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        col_unique_cnt = {}
        for col in df.columns:
            if df[col].unique().shape[0] != df.shape[0]:
                col_unique_cnt[df[col].unique().shape[0]] = col
        max_var_col = col_unique_cnt[max(col_unique_cnt)]

        fig = DM.boxPlot(df, max_var_col)

    return fig

@app.callback(Output('Table_', 'children'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')])
def update_table(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])

    return dash_table.DataTable(
        id='table-virtualiztion',
        data=df.to_dict('records'),
        columns=[
            {'name': i, 'id': i} for i in df.columns
        ],
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'whiteSpace': 'normal'
        },
        # style_data_conditional=[
        #     {'if': {'column_id': 'index'},
        #      'width': '50px'},
        #     {'if': {'column_id': 'Year'},
        #      'width': '50px'},
        #     {'if': {'column_id': 'Country'},
        #      'width': '100px'},
        #     {'if': {'column_id': 'Continent'},
        #      'width': '70px'},
        #     {'if': {'column_id': 'Emission'},
        #      'width': '75px'},
        # ],
        virtualization=True,
        page_action='none'
        )

@app.callback(Output('Mygraph_', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')])
def update_graph(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        col_unique_cnt = {}
        for col in df.columns:
            if df[col].unique().shape[0] != df.shape[0]:
                col_unique_cnt[df[col].unique().shape[0]] = col
        max_var_col = col_unique_cnt[max(col_unique_cnt)]

        fig = DM.histPlot(df, max_var_col)

    return fig

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            daf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            daf = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            daf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return daf

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# Updated DataFrame
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return children

# Это dash-like вывод DataFrame
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return children

if __name__ == '__main__':
    app.run_server(debug=True)