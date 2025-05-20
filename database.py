import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

load_dotenv()

# Konfigurasi koneksi database
DATABASE_CONFIG = {
    "host": "ep-square-star-a1wwuhwq-pooler.ap-southeast-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_3AhjU0JPRlYi",
    "sslmode": "require"
}

# Buat connection pool
connection_pool = None

def init_db_pool():
    global connection_pool
    connection_pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **DATABASE_CONFIG
    )

def get_db():
    if connection_pool is None:
        init_db_pool()
    
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)

# Alternatif: Untuk koneksi langsung tanpa pooling
def get_db_connection():
    return psycopg2.connect(os.getenv("NEON_DATABASE_URL_UNPOOLED"), cursor_factory=RealDictCursor)
