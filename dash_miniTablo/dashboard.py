import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_miniTablo.utils import parse_contents
from dash_miniTablo.config_modules import get_table_config


def init_dashboard(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dashapp/',
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )

    dash_app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="banner",
                className="banner",
                children=[html.Img(src=dash_app.get_asset_url("uglylogo.png"))],
            ),
            html.Div(
                id="right-half",
                children=[html.Div([
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
            }),
        html.Div(id='table'),

    ])]),
            init_callbacks(dash_app)
        ])

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output('table', 'children'),
                      [Input('upload-data', 'contents'),
                      Input('upload-data', 'filename')])
    def update_table(contents, filename):
        if contents:
            # contents = contents[0]
            # filename = filename[0]
            df = parse_contents(contents, filename)

        table_conf = get_table_config(df, 'table-virtualization')
        return (dash_table.DataTable(**table_conf))


