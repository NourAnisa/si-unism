from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .database import get_db
import psycopg2

app = FastAPI()

# Setup static files dan templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, db = Depends(get_db)):
    # Query untuk grafik
    with db.cursor() as cur:
        # Grafik rata-rata poin per tahun
        cur.execute("""
            SELECT tahun_ajaran, AVG(poin) as rata_poin 
            FROM skkm_points 
            GROUP BY tahun_ajaran
            ORDER BY tahun_ajaran
        """)
        avg_points = cur.fetchall()
        
        # Grafik total poin per tahun
        cur.execute("""
            SELECT tahun_ajaran, SUM(poin) as total_poin 
            FROM skkm_points 
            GROUP BY tahun_ajaran
            ORDER BY tahun_ajaran
        """)
        sum_points = cur.fetchall()
    
    return templates.TemplateResponse("landing.html", {
        "request": request,
        "avg_points": avg_points,
        "sum_points": sum_points
    })

# Include router lainnya
from .auth import router as auth_router
from .views.mahasiswa import router as mahasiswa_router
from .views.dosen import router as dosen_router

app.include_router(auth_router, prefix="/auth")
app.include_router(mahasiswa_router, prefix="/mahasiswa")
app.include_router(dosen_router, prefix="/dosen")