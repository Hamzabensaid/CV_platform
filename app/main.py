from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import cv

app = FastAPI(
    title="CV API",
    version="1.0.0",
)

# CORS pour autoriser le frontend à appeler l’API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines (à restreindre plus tard si besoin)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes CV
app.include_router(cv.router, prefix="/api/v1/cv", tags=["CV"])