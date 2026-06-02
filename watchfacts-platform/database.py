import uuid
import json
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.sqlite import JSON

# Database Configuration
DATABASE_URL = "sqlite:///watchfacts.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------------------------------------------------------
# ORM Models
# -----------------------------------------------------------------------------

class Dealer(Base):
    __tablename__ = "dealers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    trust_score = Column(Float, default=0.0) # 0-100
    tier = Column(Integer, default=1)        # 1-3
    kyc_status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="dealer")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dealer_id = Column(String, ForeignKey("dealers.id"))
    brand = Column(String)
    model = Column(String)
    reference = Column(String)
    dial_color = Column(String)
    nickname = Column(String)
    price_usd = Column(Float)
    condition_score = Column(Integer)
    box = Column(Boolean)
    papers = Column(Boolean)
    status = Column(String, default="draft")
    source_type = Column(String)
    raw_text = Column(Text)
    exception_flags = Column(Integer, default=0)
    ai_confidence = Column(Float, default=0.0)
    certification_status = Column(String, default="none")
    created_at = Column(DateTime, default=datetime.utcnow)

    dealer = relationship("Dealer", back_populates="listings")
    exceptions = relationship("ExceptionRecord", back_populates="listing")

class MasterCatalog(Base):
    __tablename__ = "master_catalog"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brand = Column(String, nullable=False)
    model = Column(String)
    reference = Column(String, nullable=False)
    dial_color = Column(String)
    nickname = Column(String)
    is_never_collapse = Column(Boolean, default=False)

class ExceptionRecord(Base):
    __tablename__ = "exceptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String, ForeignKey("listings.id"))
    exception_flags = Column(Integer)
    extracted_data = Column(JSON)
    corrected_data = Column(JSON)
    ai_proposal = Column(JSON)
    ai_confidence = Column(Float)
    status = Column(String, default="pending")
    reviewed_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing", back_populates="exceptions")

# -----------------------------------------------------------------------------
# Database Initialization & Seeding
# -----------------------------------------------------------------------------

def init_db():
    """Create all tables and seed master catalog data."""
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # Check if catalog is already seeded
        if session.query(MasterCatalog).count() > 0:
            print("Database already initialized and seeded.")
            return

        print("Seeding master catalog with Rolex data...")
        catalog_entries = [
            {"brand": "Rolex", "model": "Submariner", "reference": "116610LN", "dial_color": "Black", "nickname": None, "is_never_collapse": False},
            {"brand": "Rolex", "model": "Submariner", "reference": "116610LV", "dial_color": "Green", "nickname": "Hulk", "is_never_collapse": False},
            {"brand": "Rolex", "model": "Oyster Perpetual", "reference": "126000", "dial_color": "Tiffany", "nickname": None, "is_never_collapse": True},
            {"brand": "Rolex", "model": "Oyster Perpetual", "reference": "126000", "dial_color": "Yellow", "nickname": None, "is_never_collapse": False},
            {"brand": "Rolex", "model": "Oyster Perpetual", "reference": "126000", "dial_color": "Multicolor", "nickname": "Celebration", "is_never_collapse": True},
            {"brand": "Rolex", "model": "Oyster Perpetual", "reference": "126000", "dial_color": "Green", "nickname": None, "is_never_collapse": False},
            {"brand": "Rolex", "model": "Daytona", "reference": "116500LN", "dial_color": "White", "nickname": "Panda", "is_never_collapse": False},
            {"brand": "Rolex", "model": "Daytona", "reference": "116500LN", "dial_color": "Black", "nickname": None, "is_never_collapse": False},
            {"brand": "Rolex", "model": "GMT-Master II", "reference": "126710BLRO", "dial_color": "Black", "nickname": "Pepsi", "is_never_collapse": False}, # Note: Bezel is Blue/Red, Dial is typically Black
            {"brand": "Rolex", "model": "GMT-Master II", "reference": "126710BLNR", "dial_color": "Black", "nickname": "Batman", "is_never_collapse": False},
        ]

        for entry in catalog_entries:
            mc = MasterCatalog(**entry)
            session.add(mc)

        session.commit()
        print("Database initialization complete.")
    except Exception as e:
        session.rollback()
        print(f"Error initializing DB: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
