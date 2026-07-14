from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import instansi, tusi, rekomendasi, tindak_lanjut, program_kerja

app = FastAPI(
    title="TKPSDA WS Seputih Sekampung - Monitoring API",
    description="API CRUD untuk data monitoring tindak lanjut rekomendasi TKPSDA",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(instansi.router)
app.include_router(tusi.router)
app.include_router(rekomendasi.router)
app.include_router(tindak_lanjut.router)
app.include_router(program_kerja.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "TKPSDA Monitoring API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
