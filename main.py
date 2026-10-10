import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.database.session import engine, Base, SessionLocal
from backend.app.api.v1.api import api_router
from backend.app.models.models import TransactionModel, AccountModel, DeviceModel
from backend.app.services.ingestion.generator import dataset_generator
from backend.app.services.ingestion.pipeline import pipeline
from backend.app.services.detection.anomaly_model import anomaly_model
from backend.app.services.cryptography.pqc_service import pqc_provider

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Financial Fraud Detection, Investigation & Quantum-Safe Security. Research & Hackathon Prototype.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    """Initializes database schema and auto-seeds initial synthetic datasets if empty."""
    logger.info("Initializing QuantumShield Finance database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        tx_count = db.query(TransactionModel).count()
        if tx_count == 0:
            logger.info("Database is empty. Generating and seeding 5 synthetic stress-test scenarios...")
            dataset = dataset_generator.generate_all_datasets()
            
            # Seed accounts
            for acc in dataset["accounts"]:
                dt = datetime.datetime.fromisoformat(acc["created_at"].replace("Z", "+00:00"))
                a = AccountModel(
                    id=acc["id"],
                    customer_name=acc["customer_name"],
                    customer_email=acc["customer_email"],
                    risk_profile=acc["risk_profile"],
                    balance=acc["balance"],
                    created_at=dt
                )
                db.add(a)

            # Seed devices
            for dev in dataset["devices"]:
                d = DeviceModel(
                    id=dev["id"],
                    device_type=dev["device_type"],
                    fingerprint=dev["fingerprint"],
                    is_emulator=dev["is_emulator"],
                    first_seen=datetime.datetime.utcnow()
                )
                db.add(d)
            db.commit()

            # Pre-train Isolation Forest on normal baseline transactions
            normal_txs = dataset["scenarios"]["NORMAL"]
            anomaly_model.fit(normal_txs)

            # Process all scenario transactions through pipeline
            for tx in dataset["transactions"]:
                pipeline.process_transaction(
                    db=db,
                    tx_data=tx,
                    ground_truth_label=tx["is_synthetic_ground_truth_fraud"],
                    fraud_type=tx.get("fraud_type")
                )

            logger.info(f"Database successfully seeded with {len(dataset['transactions'])} transactions.")
        else:
            logger.info(f"Database already contains {tx_count} transactions. Pre-fitting anomaly model on baseline...")
            normal_db_txs = db.query(TransactionModel).filter(TransactionModel.scenario == "NORMAL").all()
            if normal_db_txs:
                records = [{
                    "amount": t.amount,
                    "timestamp": t.timestamp,
                    "channel": t.channel
                } for t in normal_db_txs]
                anomaly_model.fit(records)

    except Exception as e:
        logger.error(f"Error during startup seeding: {e}")
    finally:
        db.close()

@app.get("/")
def root_status():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "pqc_status": pqc_provider.get_capabilities()["status"],
        "disclaimer": "RESEARCH / HACKATHON PROTOTYPE ONLY. Not a certified production banking system. No real funds moved."
    }
