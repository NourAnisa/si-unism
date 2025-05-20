from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    nama: str
    email: str
    password: str
    role: str  # 'mahasiswa' atau 'dosen'

class UserLogin(BaseModel):
    email: str
    password: str

class SKKMPoint(BaseModel):
    user_id: int
    kategori: str
    capaian: str
    tingkat: str
    poin: int
    tahun_ajaran: str

class GoogleScholarID(BaseModel):
    user_id: int
    scholar_id: str

class Publication(BaseModel):
    user_id: int
    title: str
    journal: str
    year: int
    citation_count: int