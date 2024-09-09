from postgres_db import PostgresDB
import pandas as pd
from tqdm import tqdm

db = PostgresDB(dbname="postgres", user="postgres", password="postgres")
db.delete_db()
db.create_table()
db.init_vector_index()

def load_and_index(path):
    df = pd.read_csv(path)
    df.dropna(inplace=True, subset=['Description'])
    print(df.shape)
    for index, row in tqdm(df.iterrows(), total=len(df)):

        company_data = {
            'company': row['Company'],
            'country': row['Country'],
            'revenue': '',
            'head_count': str(row['Head Count']),
            'funding': '',
            'sector': str(row['Sector']),
            'description': row['Description'],
            'news_headlines': ''
        }
        db.insert_company(company_data)

    print(db.get_num_rows())

    db.close_connection()

if __name__ == '__main__':
    load_and_index('../2023-02-27-yc-companies - finalusabledata.csv')