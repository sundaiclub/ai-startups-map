import psycopg2
from psycopg2 import sql
import uuid
from pgvector.psycopg2 import register_vector
from encoder import Encoder

class PostgresDB:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        register_vector(self.conn)
        self.model = Encoder()
    
    def init_vector_index(self):
        self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        self.conn.commit()


    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            company TEXT,
            country TEXT,
            revenue TEXT,
            head_count INTEGER,
            funding TEXT,
            sector TEXT,
            description TEXT,
            news_headlines TEXT,
            description_vector vector(384)
        )
        """)
        self.init_vector_index()
        self.conn.commit()

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def insert_company(self, company_data):
        # Check if the company already exists
        self.cursor.execute("SELECT id FROM companies WHERE company = %s", (company_data['company'],))
        if self.cursor.fetchone() is not None:
            print(f"Company '{company_data['company']}' already exists. Skipping insertion.")
            return None

        company_id = self.generate_unique_id()
        description_vector = self.model.batch_encode(company_data['description']).tolist()[0]
        try:
            self.cursor.execute("""
            INSERT INTO companies (id, company, country, revenue, head_count, funding, sector, description, news_headlines, description_vector)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                company_id,
                company_data['company'],
                company_data['country'],
                company_data['revenue'],
                int(company_data['head_count'].replace(',', '')),
                company_data['funding'],
                company_data['sector'],
                company_data['description'],
                company_data['news_headlines'],
                description_vector
            ))
            self.conn.commit()
            return company_id
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error inserting company: {e}")
            return None

    def get_company_by_id(self, company_id):
        self.cursor.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
        return self.cursor.fetchone()

    def get_companies_by_country(self, country):
        self.cursor.execute("SELECT * FROM companies WHERE country = %s", (country,))
        return self.cursor.fetchall()

    def get_companies_by_sector(self, sector):
        self.cursor.execute("SELECT * FROM companies WHERE sector ILIKE %s", (f"%{sector}%",))
        return self.cursor.fetchall()

    def update_company(self, company_id, update_data):
        update_query = sql.SQL("UPDATE companies SET {} WHERE id = %s").format(
            sql.SQL(', ').join(sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in update_data.keys())
        )
        self.cursor.execute(update_query, {**update_data, 'id': company_id})
        self.conn.commit()

    def delete_company(self, company_id):
        self.cursor.execute("DELETE FROM companies WHERE id = %s", (company_id,))
        self.conn.commit()

    def search_similar_descriptions(self, query_description, limit=5):
        query_vector = self.model.batch_encode(query_description).tolist()[0]
        self.cursor.execute("""
        SELECT company, description, description_vector, description_vector <-> (%s::vector) AS distance
        FROM companies
        ORDER BY distance
        LIMIT %s;

        """, (query_vector, limit))

        return query_vector, self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
    
    def get_num_rows(self):
        self.cursor.execute("SELECT COUNT(*) FROM companies")
        return self.cursor.fetchone()[0]
    
    def delete_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS companies;")
        self.conn.commit()