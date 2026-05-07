# backend/scripts/seed_data.py
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.database import SessionLocal, init_db
from app.db.models import Product, Region, Sale

REGIONS = [
    {"name": "North", "country": "Nigeria"},
    {"name": "South", "country": "Nigeria"},
    {"name": "East", "country": "Nigeria"},
    {"name": "West", "country": "Nigeria"},
    {"name": "Lagos", "country": "Nigeria"},
    {"name": "Abuja", "country": "Nigeria"},
]

PRODUCTS = [
    {"name": "Laptop Pro 15", "category": "Electronics", "unit_price": 850000},
    {"name": "Wireless Headphones", "category": "Electronics", "unit_price": 45000},
    {"name": "Office Chair Deluxe", "category": "Furniture", "unit_price": 120000},
    {"name": "Standing Desk", "category": "Furniture", "unit_price": 180000},
    {"name": "Accounting Software", "category": "Software", "unit_price": 75000},
    {"name": "Project Manager Pro", "category": "Software", "unit_price": 55000},
    {"name": "Mechanical Keyboard", "category": "Electronics", "unit_price": 65000},
    {"name": "4K Monitor", "category": "Electronics", "unit_price": 320000},
    {"name": "Executive Desk", "category": "Furniture", "unit_price": 250000},
    {"name": "Cloud Storage Plan", "category": "Software", "unit_price": 25000},
]

# Regional sales weights — Lagos and Abuja sell more
REGION_WEIGHTS = {
    "North": 0.12,
    "South": 0.15,
    "East": 0.13,
    "West": 0.15,
    "Lagos": 0.25,
    "Abuja": 0.20,
}


def seed():
    init_db()
    db = SessionLocal()
    try:
        if db.query(Sale).count() > 0:
            print("Database already seeded — skipping")
            return

        # Insert regions
        region_objects = {}
        for r in REGIONS:
            region = Region(**r)
            db.add(region)
            db.flush()
            region_objects[r["name"]] = region

        # Insert products
        product_objects = []
        for p in PRODUCTS:
            product = Product(**p)
            db.add(product)
            db.flush()
            product_objects.append(product)

        # Generate 18 months of daily sales (realistic volume)
        start_date = datetime(2024, 1, 1)
        sales_count = 0

        for day_offset in range(548):  # 18 months
            sale_date = start_date + timedelta(days=day_offset)

            # Skip some days to make data realistic (not every product sells daily)
            daily_transactions = random.randint(3, 12)

            for _ in range(daily_transactions):
                product = random.choice(product_objects)
                region_name = random.choices(
                    list(REGION_WEIGHTS.keys()),
                    weights=list(REGION_WEIGHTS.values()),
                )[0]
                region = region_objects[region_name]
                quantity = random.randint(1, 5)
                # Add slight price variation (+/- 5%)
                price_variation = random.uniform(0.95, 1.05)
                amount = round(product.unit_price * quantity * price_variation, 2)

                sale = Sale(
                    product_id=product.id,
                    region_id=region.id,
                    quantity=quantity,
                    amount=amount,
                    sale_date=sale_date,
                )
                db.add(sale)
                sales_count += 1

        db.commit()
        print(f"✅ Seeded {len(REGIONS)} regions, {len(PRODUCTS)} products, {sales_count} sales")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()