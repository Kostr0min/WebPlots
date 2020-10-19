def get_table_config(df=None, type='table-virtualization'):
    #col_list = df.columns
    table_conf = {}
    if df is not None:
        if type == 'table-virtualization':
            table_conf = dict(
                id='table-virtualiztion',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                ],
                data=df.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="multi",
                row_selectable="multi",
                fixed_rows={'headers': False},
                style_cell={'whiteSpace': 'normal'},
                row_deletable=True,
                selected_columns=[],
                style_table={'overflowX': 'auto'},
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            )

    return table_conf