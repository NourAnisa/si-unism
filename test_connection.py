from fastapi import APIRouter, Depends, HTTPException
from .database import get_db
import psycopg2
import logging

router = APIRouter(tags=["Diagnostic"])
logger = logging.getLogger(__name__)

@router.get("/test-db-connection", summary="Test database connectivity")
async def test_db_connection(db = Depends(get_db)):
    """
    Endpoint khusus untuk menguji koneksi database dengan 3 level pengecekan:
    1. Koneksi dasar
    2. Query sederhana
    3. Query ke tabel spesifik
    """
    try:
        # Level 1: Cek koneksi dasar
        with db.cursor() as cur:
            # Level 2: Query sistem
            cur.execute("SELECT version()")
            pg_version = cur.fetchone()
            logger.info(f"PostgreSQL version: {pg_version}")

            # Level 3: Query tabel aplikasi
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [row['table_name'] for row in cur.fetchall()]
            logger.info(f"Tables found: {tables}")

        return {
            "status": "success",
            "postgres_version": pg_version,
            "tables_available": tables,
            "connection": "stable"
        }
        
    except psycopg2.OperationalError as e:
        logger.error(f"Connection failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "type": "operational",
                "message": str(e)
            }
        )
    except psycopg2.ProgrammingError as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "type": "query",
                "message": "Table might not exist"
            }
        )
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "critical",
                "type": "unknown",
                "message": "Internal server error"
            }
        )
