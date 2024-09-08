from postgres_db import PostgresDB
import pandas as pd

db = PostgresDB(dbname="postgres", user="postgres", password="postgres")
db.delete_db()
db.create_table()
db.init_vector_index()

def load_and_index(path):
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        company_data = {
            'company': row['Company'],
            'country': row['Country'],
            'revenue': row['Revenue'],
            'head_count': row['Head Count'],
            'funding': row['Funding'],
            'sector': row['Sector'],
            'description': row['Description'],
            'news_headlines': row['News Headlines']
        }
        db.insert_company(company_data)

    print(db.get_num_rows())

    db.close_connection()

if __name__ == '__main__':
    load_and_index('../samplecompanies - Sheet1.csv')