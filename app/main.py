from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import cv_routes, test_errors, user_routes 
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.utils import error_handler
from fastapi.security import OAuth2PasswordBearer


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

# Security scheme for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

app.add_exception_handler(StarletteHTTPException, error_handler.http_exception_handler)
app.add_exception_handler(RequestValidationError, error_handler.validation_exception_handler)
app.add_exception_handler(Exception, error_handler.generic_exception_handler)


# Inclure les routes CV
app.include_router(cv_routes.router, prefix="/api/v1/cv", tags=["CV"])
app.include_router(test_errors.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1/users")

