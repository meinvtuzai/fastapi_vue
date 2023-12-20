import pandas as pd
import os
from db.session import SessionLocal, engine
from core.config import settings

db = SessionLocal()
database_name = settings.SQL_DATABASE
sql = f"""
    SELECT TABLE_NAME FROM information_schema.`TABLES` WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_NAME != 'alembic_version'
"""
rows = db.execute(sql).fetchall()
print(len(rows), rows)
for table in rows:
    table_name = table[0]
    sql = f"""
    SELECT * FROM {database_name}.{table_name}
    """

    df = pd.read_sql(sql, con=engine)
    dir_path = os.path.join(os.path.dirname(__file__), "init_data")
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{table_name.replace(settings.SQL_TABLE_PREFIX, '', 1)}.csv")
    print(file_path)
    df.to_csv(file_path, index=0)
