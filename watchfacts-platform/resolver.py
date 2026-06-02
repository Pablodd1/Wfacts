import json
from database import SessionLocal, ExceptionRecord, Listing, MasterCatalog

# Bitmask decoder
def decode_flags(flags: int) -> list:
    flag_names = {
        1: "REF_NOT_FOUND",
        2: "REF_MULTIPLE",
        4: "COLOR_NOT_FOUND",
        8: "COLOR_MULTIPLE",
        16: "PRICE_NOT_FOUND",
        32: "PRICE_MULTIPLE",
        64: "AI_DISCREPANCY",
        128: "CATALOG_MISMATCH"
    }
    return [name for bit, name in flag_names.items() if flags & bit]

def resolve_exception(exception_id: str) -> dict:
    session = SessionLocal()
    try:
        ex = session.query(ExceptionRecord).filter(ExceptionRecord.id == exception_id).first()
        if not ex:
            return {"error": "Exception not found"}

        listing = session.query(Listing).filter(Listing.id == ex.listing_id).first()
        raw_text = listing.raw_text.lower()

        proposed = {
            "proposed_reference": None,
            "proposed_dial_color": None,
            "proposed_price_usd": None,
            "confidence": 0.0,
            "reasoning": ""
        }

        # 1. Nickname resolution
        if "hulk" in raw_text:
            proposed["proposed_reference"] = "116610LV"
            proposed["proposed_dial_color"] = "Green"
            proposed["confidence"] = 0.95
            proposed["reasoning"] = "Detected nickname 'Hulk'. Maps to Submariner 116610LV Green dial."
        elif "pepsi" in raw_text:
            proposed["proposed_reference"] = "126710BLRO"
            proposed["proposed_dial_color"] = "Black"
            proposed["confidence"] = 0.95
            proposed["reasoning"] = "Detected nickname 'Pepsi'. Maps to GMT-Master II 126710BLRO."
        elif "batman" in raw_text:
            proposed["proposed_reference"] = "126710BLNR"
            proposed["proposed_dial_color"] = "Black"
            proposed["confidence"] = 0.95
            proposed["reasoning"] = "Detected nickname 'Batman'. Maps to GMT-Master II 126710BLNR."

        # 2. Turquoise / Tiffany edge case
        elif "126000" in raw_text and ("turquoise" in raw_text or "tiffany" in raw_text):
            # Check catalog for 126000
            catalog_entries = session.query(MasterCatalog).filter(MasterCatalog.reference == "126000").all()
            dial_colors = [c.dial_color.lower() for c in catalog_entries if c.dial_color]

            if "tiffany" in dial_colors and "turquoise" not in dial_colors:
                 proposed["proposed_reference"] = "126000"
                 proposed["proposed_dial_color"] = "Tiffany"
                 proposed["confidence"] = 0.92
                 proposed["reasoning"] = "Listing text stated 'turquoise' for reference 126000. Catalog has 'Tiffany' but not 'Turquoise'. Dealer community frequently uses 'turquoise' interchangeably with Tiffany on this reference. 'Tiffany' is a never-collapse rule."

        # 3. Price extraction (simple mock)
        if "k" in raw_text:
            try:
                import re
                match = re.search(r'\$(\d+(?:\.\d+)?)k', raw_text)
                if match:
                    proposed["proposed_price_usd"] = float(match.group(1)) * 1000
                    if proposed["confidence"] == 0:
                        proposed["confidence"] = 0.8
                        proposed["reasoning"] = "Extracted price from 'k' suffix format."
                    else:
                        proposed["reasoning"] += " Extracted price from 'k' suffix format."
            except Exception:
                pass

        # 4. Catalog mismatch resolution
        elif "126610ln" in raw_text and "blue" in raw_text:
             proposed["proposed_reference"] = "126610LN"
             proposed["proposed_dial_color"] = "Black"
             proposed["confidence"] = 0.85
             proposed["reasoning"] = "Reference 126610LN is cataloged only with a Black dial. 'Blue' is likely a mistake by the dealer."

        return proposed
    finally:
        session.close()

def run_batch_resolver(limit: int = 100):
    session = SessionLocal()
    try:
        exceptions = session.query(ExceptionRecord).filter(ExceptionRecord.status == "pending").limit(limit).all()
        print(f"Running batch resolver on {len(exceptions)} exceptions...")

        resolved_count = 0
        for ex in exceptions:
            result = resolve_exception(ex.id)
            if result.get("confidence", 0) > 0.8:
                ex.ai_proposal = result
                ex.status = "ai_resolved"
                resolved_count += 1

        session.commit()
        print(f"Batch resolution complete. Auto-resolved {resolved_count}/{len(exceptions)} exceptions.")
    finally:
        session.close()

if __name__ == "__main__":
    run_batch_resolver(10)
