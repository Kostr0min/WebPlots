import dash
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
import numpy as np
import dbmodules as dbm
from modules import DashModul
import layout
from config_modules import get_table_config
import tables
import flask

DM = DashModul()

flask_app = flask.Flask(__name__)

app = dash.Dash(
    __name__, server=flask_app,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

engine, setting_table, connection, metadata = dbm.connection_method()

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = layout.get_layout()


@app.callback(Output("loading-output-2", "children"), [Input("t_status", "value")])
def input_triggers_nested(value):
    print(value)
    # time.sleep(1)
    return value


@app.callback([Output("load-val", "style"),
               Output("session_code", "style")],
              [Input('upload-data', 'contents')])
def update_load_button(contents):
    if contents is not None:
        return dict(), dict()
    else:
        return dict(display='none'), dict(display='none')
# from config_modules import change_range


@app.callback([Output('data-slider', 'min'),
               Output('data-slider', 'max'),
               Output('data-slider', 'marks')],
              [Input('dropdown_table_rangeColumn', 'value'),
               Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def change_range(dropdown_value, contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        slider_values = df[dropdown_value].values
        min_val = slider_values.min()
        max_val = slider_values.max()
        # controversial point
        point_range = (slider_values.max() - slider_values.min())//10
        data_points = np.arange(slider_values.min(), slider_values.max(), point_range)
        marks = {str(data_point): str(data_point) for data_point in data_points}
        return min_val, max_val, marks


@app.callback([Output('dropdown_table_rangeColumn', 'options'),
               Output('dropdown_table_plotColumn', 'options')],
              [Input('dropdown_table_filterColumn', 'value'),
               Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(filter_columns, contents, filename):
    # df = pd.DataFrame()
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        if filter_columns is not None:
            return [{'label': i, 'value': i} for i in filter_columns], \
                   [{'label': i, 'value': i} for i in filter_columns]
        else:
            return [{'label': i, 'value': i} for i in df.columns], [{'label': i, 'value': i} for i in df.columns]


@app.callback(Output('dropdown_table_filterColumn', 'options'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    df = pd.DataFrame()
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
    return [{'label': i, 'value': i} for i in df.columns]


@app.callback(Output('t_status', 'children'),
              [Input('upload-data', 'contents')])
def update_status(contents):
    load_status = False
    if not contents:
        load_status = True
    return load_status


parse_data = tables.parse_data


@app.callback([Output('tabs-example-content', 'figure'),
               Output('Table_', 'children'),
               Output('describe_table', 'children')],
              [
    Input('tabs-example', 'value'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('dropdown_table_filterColumn', 'value'),
    Input('dropdown_table_rangeColumn', 'value'),
    Input('data-slider', 'value'),
    Input('input1', 'value'),
    Input('input2', 'value'),
    Input('dropdown_table_plotColumn', 'value')])
def update_table(flag, contents, filename, columns, range_column, _range, _lower, _upper, plot_column):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # Bad approach, a good one coming soon...
        if range_column and _range:
            df = df[df[range_column].isin(_range)]
        elif range_column and _lower and _upper:
            df = df[df[range_column].isin([int(_lower), int(_upper)])]
    if columns:
        df = df[columns]
        if range_column and _range:
            df = df[df[range_column].isin(_range)]
        elif range_column and _lower and _upper:
            df = df[df[range_column].isin([int(_lower), int(_upper)])]
    col_list = df.columns

    describe_df = df.describe().round(3)
    describe_index_df = pd.DataFrame({'stat': ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']})
    describe_df = pd.concat([describe_index_df.reset_index(drop=True), describe_df.reset_index(drop=True)], axis=1)
    describe_df = describe_df.set_index(describe_df['stat'])
    describe_col_list = describe_df.columns

    if flag == 'HeatMap':
        fig = DM.heatmapPlot(df)
    elif flag == 'HistPlot':
        fig = DM.histPlot(df[plot_column].values)
    elif flag == 'boxPlot':
        fig = DM.boxPlot(df[plot_column].values)
    elif flag == 'distPlot':
        fig = DM.distPlot(df[plot_column].values, plot_column)

    table_conf = get_table_config(df, col_list, 'table-virtualization')
    describe_table_conf = get_table_config(describe_df, describe_col_list, 'describe_table-virtualization')
    return (fig, dash_table.DataTable(**table_conf),
            dash_table.DataTable(**describe_table_conf))


@app.callback([Output('dropdown_table_filterColumn', 'value'),
               Output('dropdown_table_rangeColumn', 'value'),
               Output('data-slider', 'value'),
               Output('input1', 'value'),
               Output('input2', 'value'),
               Output('dropdown_table_plotColumn', 'value')],
              [Input('load-val', 'n_clicks'),
               Input('session_code', 'value'),
               Input('upload-data', 'contents'),
               Input('upload-data', 'filename')]
              )
def update_output(n_clicks, ses_code, contents, filename):
    if n_clicks > 0:
        settings = [None]*7
        if ses_code:
            settings = dbm.select_values(setting_table, connection, ses_code)
        params_list = ['filter_columns', 'range_column', 'data_slider', 'input_1', 'input_2',
                       'column_for_plots', 'session_code']
        filter_column, range_column, _range, _lower, _upper, plot_column, ses_code = [settings[x] for x in params_list]
        if filter_column is not None:
            filter_column = list(filter_column.keys())
        if _range is not None:
            _range = sorted(list(_range.values()))
        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            range_column = df.columns[range_column]
            plot_column = df.columns[plot_column]
        return filter_column, range_column, _range, _lower, _upper, plot_column


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks'),
     Input('upload-data', 'contents'),
     Input('upload-data', 'filename')
     ],
    [State('dropdown_table_filterColumn', 'value'),
     State('data-slider', 'value'),
     State('input1', 'value'),
     State('input2', 'value'),
     State('dropdown_table_rangeColumn', 'value'),
     State('dropdown_table_plotColumn', 'value')])
def update_output(n_clicks, contents, filename, filter_column, _range, _lower,  _upper, range_column, plot_column):
    ses_code = ''
    if n_clicks > 0:
        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            ses_code = dbm.insert_values([filter_column, range_column, _range, _lower, _upper, plot_column],
                                         setting_table, connection, df)
        n_clicks -= 1
    return f'Ses code {ses_code}'


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=80)
