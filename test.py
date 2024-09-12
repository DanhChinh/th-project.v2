
import pandas as pd
from sqlalchemy import create_engine


def connect_database():
    engine = create_engine('mysql+mysqlconnector://root:thuhuyen123@localhost:3306/qlearning_database')
    return engine

def read_database_to_dataframe(engine, table_name):
    df =  pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
    return df
def save_dataframe_to_database(engine, table_name, dataframe):
    dataframe.to_sql(table_name, engine, if_exists='replace', index=False)



# df = read_database_to_dataframe(engine, "black_table")

engine = connect_database()
df = pd.read_sql_query(f"SELECT * FROM black_table WHERE value != 0;", engine)
print(df)
print()
df = pd.read_sql_query(f"SELECT * FROM red_table WHERE value != 0;", engine)
print(df)