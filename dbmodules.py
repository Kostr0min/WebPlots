from flask_sqlalchemy import SQLAlchemy
import dash
import sqlalchemy as db
import random


def connection_method():

    hostname = "localhost"
    dbname = "new_schema"
    jdbcPort = 3306
    username = "root"
    password = "root"
    jdbc_url = "mysql+mysqlconnector://{0}:{1}/{2}?user={3}&password={4}".format(hostname, jdbcPort, dbname,
                                                                              username, password)
    engine = db.create_engine(jdbc_url)
    connection = engine.connect()
    metadata = db.MetaData()
    setting_table = db.Table('session_settings', metadata, autoload=True, autoload_with=engine)
    return(engine, setting_table, connection, metadata)

def get_exmpl():
    exmpl = db.Table('exmpl', metadata, autoload=True, autoload_with=engine)
    return(exmpl)

def insert_values(config_list, setting_table_, conn, df):

    filter_columns_json = config_list[0]
    data_slider_json = config_list[2]
    if config_list[0] != None:
        filter_columns_json = {key: df.columns.get_loc(key) for key in config_list[0]}

    if config_list[2] != None:
        data_slider_json = {'min': config_list[2][0], 'max': config_list[2][1]}

    if config_list[1] != None:
        config_list[1] = df.columns.get_loc(config_list[1])

    if config_list[5] != None:
        config_list[5] = df.columns.get_loc(config_list[5])


    ses_code = random.getrandbits(128)
    ins = setting_table_.insert().values(filter_columns=filter_columns_json, range_column=config_list[1],
                                        data_slider =data_slider_json, input_1=config_list[3], input_2=config_list[4],
                                         column_for_plots=config_list[5], session_code=ses_code)
    print(str(ins))
    conn.execute(ins)
    return ses_code

#engine, setting_table, connection, metadata = connection_method()

def select_values(setting_table_, conn, ses_code):
    query = db.select([setting_table_]).where(setting_table_.columns.session_code == ses_code)
    return conn.execute(query).fetchone()

