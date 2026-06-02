import random
import json
from datetime import datetime, timedelta
from faker import Faker
from database import SessionLocal, Dealer, Listing, ExceptionRecord, init_db

fake = Faker()

# Exception Flag Bitmasks
REF_NOT_FOUND = 1
COLOR_NOT_FOUND = 4
PRICE_NOT_FOUND = 16
CATALOG_MISMATCH = 128

def generate_dealers(session, num_dealers=50):
    dealers = []
    for _ in range(num_dealers):
        dealer = Dealer(
            name=fake.company(),
            phone=fake.phone_number(),
            email=fake.company_email(),
            trust_score=random.uniform(50, 100),
            tier=random.choice([1, 2, 3]),
            kyc_status=random.choice(['approved', 'pending'])
        )
        session.add(dealer)
        dealers.append(dealer)
    session.commit()
    return dealers

def generate_listings():
    init_db()
    session = SessionLocal()
    dealers = session.query(Dealer).all()
    if not dealers:
        dealers = generate_dealers(session)

    print("Generating 1,000 synthetic listings...")

    clean_count = int(1000 * 0.70)
    exception_count = 1000 - clean_count

    # 1. Generate Clean Listings (70%)
    clean_templates = [
        ("Rolex Submariner {ref} {color} dial full set ${price}", "Submariner", ["116610LN", "116610LV"], ["Black", "Green"]),
        ("FS: Rolex Daytona {ref} {color} dial ${price}", "Daytona", ["116500LN"], ["White", "Black"]),
        ("Rolex GMT {ref} {color} dial box and papers ${price}", "GMT-Master II", ["126710BLRO", "126710BLNR"], ["Black"]),
        ("Rolex OP {ref} {color} dial new ${price}", "Oyster Perpetual", ["126000"], ["Tiffany", "Yellow", "Multicolor", "Green"])
    ]

    for _ in range(clean_count):
        dealer = random.choice(dealers)
        template, model, refs, colors = random.choice(clean_templates)
        ref = random.choice(refs)
        color = random.choice(colors)
        price = random.randint(10000, 40000)
        raw_text = template.format(ref=ref, color=color, price=f"{price:,}")

        listing = Listing(
            dealer_id=dealer.id,
            brand="Rolex",
            model=model,
            reference=ref,
            dial_color=color,
            price_usd=price,
            condition_score=random.randint(85, 100),
            box=True,
            papers=True,
            status="pending_certification" if random.random() > 0.5 else "live",
            source_type="whatsapp",
            raw_text=raw_text,
            exception_flags=0,
            ai_confidence=random.uniform(0.9, 0.99),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        session.add(listing)

    # 2. Generate Exception Listings (30%)
    exception_types = [
        (REF_NOT_FOUND, "Rolex Submariner {bad_ref} Black dial full set $11,500", "11661"), # Typo in ref
        (COLOR_NOT_FOUND, "Rolex Submariner 116610LN full set $11,500", None), # Missing color
        (CATALOG_MISMATCH, "Rolex Submariner 126610LN blue dial $15,000", "126610LN"), # Wrong color for ref (should be black)
        (PRICE_NOT_FOUND, "Rolex 116500 NOS brand new 23€", "116500"), # Weird price format
        (PRICE_NOT_FOUND, "Rolex 116610LN $32,000 / €29,500", "116610LN"), # Multiple prices (could use custom flag, but PRICE_NOT_FOUND covers parsing failure)
        (0, "Rolex Hulk $18.5k", None), # Needs normalization, technically clean if AI handles nicknames
        (0, "Pepsi full set", None),    # Needs normalization
        (CATALOG_MISMATCH, "Rolex 126000 turquoise dial $12k", "126000") # The Tiffany/Turquoise edge case
    ]

    for _ in range(exception_count):
        dealer = random.choice(dealers)
        ex_flag, template_str, bad_val = random.choice(exception_types)

        if "{bad_ref}" in template_str:
            raw_text = template_str.format(bad_ref=bad_val)
            ref_val = None # Failed to extract cleanly
        else:
            raw_text = template_str
            ref_val = bad_val

        # Create Listing with exception flags
        listing = Listing(
            dealer_id=dealer.id,
            brand="Rolex" if "Rolex" in raw_text else None,
            reference=ref_val,
            status="exception",
            source_type="whatsapp",
            raw_text=raw_text,
            exception_flags=ex_flag if ex_flag != 0 else (REF_NOT_FOUND | COLOR_NOT_FOUND), # Give nicknames some flags to force review
            ai_confidence=random.uniform(0.4, 0.7),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        session.add(listing)
        session.flush() # Get listing.id

        # Create corresponding ExceptionRecord
        ex_record = ExceptionRecord(
            listing_id=listing.id,
            exception_flags=listing.exception_flags,
            extracted_data={"raw": raw_text}, # Simplified
            status="pending"
        )
        session.add(ex_record)

    session.commit()
    print("Generation complete!")
    session.close()

if __name__ == "__main__":
    generate_listings()
