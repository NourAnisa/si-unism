from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from .database import get_db
import psycopg2
from .templates import templates

router = APIRouter(dependencies=[Depends(get_db)])

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_mahasiswa(request: Request, db = Depends(get_db)):
    # Dapatkan user_id dari token
    token = request.cookies.get("access_token")
    # Decode token untuk dapatkan user_id (implementasi decode token)
    
    # Query data SKKM mahasiswa
    with db.cursor() as cur:
        cur.execute("""
            SELECT tahun_ajaran, SUM(poin) as total_poin 
            FROM skkm_points 
            WHERE user_id = %s
            GROUP BY tahun_ajaran
            ORDER BY tahun_ajaran
        """, (user_id,))
        skkm_data = cur.fetchall()
        
        # Query publikasi
        cur.execute("""
            SELECT year, COUNT(*) as jumlah_publikasi, SUM(citation_count) as total_sitasi
            FROM publications
            WHERE user_id = %s
            GROUP BY year
            ORDER BY year
        """, (user_id,))
        publications_data = cur.fetchall()
    
    return templates.TemplateResponse("mahasiswa.html", {
        "request": request,
        "skkm_data": skkm_data,
        "publications_data": publications_data
    })
