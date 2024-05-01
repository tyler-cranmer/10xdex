import psycopg2
from contextlib import contextmanager
from config import Settings

s = Settings()

@contextmanager
def get_db():
    conn = psycopg2.connect(host=s.POSTGRES_HOST, user=s.POSTGRES_USER, password=s.POSTGRES_PASSWORD, dbname=s.POSTGRES_DB)
    try:
        yield conn
    finally:
        conn.close()
