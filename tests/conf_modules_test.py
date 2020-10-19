from miniTablo.dash_miniTablo.config_modules import get_table_config
import pytest
import pandas as pd

def test_table_config():
    empty_df = pd.DataFrame()
    base_config = {'id': 'table-virtualiztion',
     'columns': [],
     'data': [],
     'editable': True,
     'filter_action': 'native',
     'sort_action': 'native',
     'sort_mode': 'multi',
     'column_selectable': 'multi',
     'row_selectable': 'multi',
     'fixed_rows': {'headers': False},
     'style_cell': {'whiteSpace': 'normal'},
     'row_deletable': True,
     'selected_columns': [],
     'style_table': {'overflowX': 'auto'},
     'selected_rows': [],
     'page_action': 'native',
     'page_current': 0,
     'page_size': 10}

    res_1 = get_table_config(None)
    res_2 = get_table_config(empty_df)

    assert res_1 == {}
    assert res_2 == base_config


