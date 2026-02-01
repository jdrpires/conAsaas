from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customers, payments, webhooks
from app.core.logging import logger

app = FastAPI(
    title="ConAssas API",
    description="API REST para integração com Asaas - Pagamentos via Cartão, Boleto e PIX",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(customers.router)
app.include_router(payments.router)
app.include_router(webhooks.router)


@app.get("/")
async def root():
    return {
        "message": "ConAssas API - Integração com Asaas",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting ConAssas API...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ConAssas API...")
