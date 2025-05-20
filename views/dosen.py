from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from .database import get_db
import psycopg2
from .templates import templates

router = APIRouter(dependencies=[Depends(get_db)])

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_dosen(request: Request, db = Depends(get_db)):
    # Query data semua mahasiswa
    with db.cursor() as cur:
        # Grafik SKKM semua mahasiswa
        cur.execute("""
            SELECT tahun_ajaran, AVG(poin) as rata_poin 
            FROM skkm_points 
            GROUP BY tahun_ajaran
            ORDER BY tahun_ajaran
        """)
        avg_skkm = cur.fetchall()
        
        # Grafik publikasi
        cur.execute("""
            SELECT year, COUNT(*) as jumlah_publikasi
            FROM publications
            WHERE year BETWEEN 2019 AND 2025
            GROUP BY year
            ORDER BY year
        """)
        publications = cur.fetchall()
    
    return templates.TemplateResponse("dosen.html", {
        "request": request,
        "avg_skkm": avg_skkm,
        "publications": publications
    })