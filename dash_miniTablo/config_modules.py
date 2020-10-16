import numpy as np

def change_range(dropdown_value, df):
    min_val, max_val, marks, point_range, data_points = [None] * 5
    slider_values = df[dropdown_value].values
    if slider_values:
        min_val = slider_values.min()
        max_val = slider_values.max()
        point_range = (slider_values.max() - slider_values.min())//10
        data_points = np.arange(slider_values.min(), slider_values.max(), point_range)
        marks = {str(data_point): str(data_point) for data_point in data_points}

    return min_val, max_val, marks


def all_filter_columns(dropdown_value, df):
    min_val, max_val, marks, point_range, data_points = [None] * 5
    slider_values = df[dropdown_value].values
    min_val = slider_values.min()
    max_val = slider_values.max()
    point_range = (slider_values.max() - slider_values.min())//10
    data_points = np.arange(slider_values.min(), slider_values.max(), point_range)
    marks = {str(data_point): str(data_point) for data_point in data_points}

    return min_val, max_val, marks, [{'label': i, 'value': i} for i in df.columns], [{'label': i, 'value': i} for i in df.columns], \
           [{'label': i, 'value': i} for i in df.columns]


def get_table_config(df, col_list, type):
    if type == 'table-virtualization':
        table_conf = dict(
            id='table-virtualiztion',
            data=df.to_dict('records'),
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'center'
                } for c in col_list
            ],
            fixed_rows={'headers': True},
            style_cell={
                'minWidth': 150, 'maxWidth': 150, 'width': 150
            }
        )
    elif type == 'describe_table-virtualization':
        table_conf = dict(
        id='describe_table-virtualiztion',
        data=df.to_dict('records'),
        columns=[
            {'name': i, 'id': i} for i in df.columns
        ],
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'stat',
                },
                'backgroundColor': 'dodgerblue',
                'color': 'white'
            },
        ],
        style_cell_conditional=[{
                'if': {'column_id': c},
                      'textAlign': 'center'
                } for c in col_list
            ],
        style_data={
            'width': '110px',
            'maxWidth': '110px',
            'minWidth': '110px',
        },
        style_table={
            'overflowX': 'auto'
        },
        style_cell={
            'whiteSpace': 'normal',
        },
        virtualization=True,
        page_action='none'
    )

    return table_conf