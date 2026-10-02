"""Create data/harbor.db: a small, fixed dataset for Harbor Supply Co., a marine supply store.

Run once (it's safe to rerun; it rebuilds from scratch):
    python data/seed_db.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("harbor.db")

CUSTOMERS = [
    (1, "Ana Reyes", "ana@example.com", "Ballard"),
    (2, "Marcus Webb", "marcus@example.com", "Tacoma"),
    (3, "Priya Nair", "priya@example.com", "Everett"),
    (4, "Tom Okafor", "tom@example.com", "Bremerton"),
    (5, "Lena Park", "lena@example.com", "Anacortes"),
]

PRODUCTS = [  # id, sku, name, category, price, stock, reorder_level
    (1, "LJ-200", "Offshore life jacket", "safety", 129.00, 14, 10),
    (2, "FL-050", "Flare kit (6 pack)", "safety", 64.50, 3, 8),
    (3, "AN-120", "Galvanized anchor 12 kg", "hardware", 89.99, 6, 4),
    (4, "RP-030", "Nylon dock line 30 ft", "rigging", 24.95, 40, 15),
    (5, "BL-012", "Bilge pump 12V", "engine", 149.00, 2, 5),
    (6, "VHF-10", "Handheld VHF radio", "electronics", 219.00, 7, 5),
    (7, "FE-002", "Marine fire extinguisher", "safety", 54.00, 0, 6),
    (8, "BT-100", "Deep-cycle battery 100Ah", "electronics", 279.00, 9, 4),
    (9, "WX-500", "Teak oil 500 ml", "maintenance", 19.50, 25, 10),
    (10, "PR-044", "Stainless propeller 14x19", "engine", 489.00, 1, 2),
]

ORDERS = [  # id, customer_id, placed, status
    (1001, 1, "2026-09-02", "delivered"),
    (1002, 2, "2026-09-05", "shipped"),
    (1003, 3, "2026-09-08", "processing"),
    (1004, 1, "2026-09-10", "shipped"),
    (1005, 4, "2026-09-12", "cancelled"),
    (1006, 5, "2026-09-15", "processing"),
    (1007, 2, "2026-09-18", "delivered"),
    (1008, 3, "2026-09-20", "backordered"),
]

ORDER_ITEMS = [  # order_id, product_id, qty
    (1001, 1, 2), (1001, 4, 4),
    (1002, 6, 1),
    (1003, 3, 1), (1003, 9, 2),
    (1004, 8, 1), (1004, 5, 1),
    (1005, 10, 1),
    (1006, 2, 2), (1006, 1, 1),
    (1007, 4, 6),
    (1008, 7, 3),
]


def build(path: Path = DB) -> Path:
    path.unlink(missing_ok=True)
    con = sqlite3.connect(path)
    con.executescript("""
        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
        CREATE TABLE products (id INTEGER PRIMARY KEY, sku TEXT UNIQUE, name TEXT, category TEXT,
                               price REAL, stock INTEGER, reorder_level INTEGER);
        CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id),
                             placed TEXT, status TEXT);
        CREATE TABLE order_items (order_id INTEGER REFERENCES orders(id),
                                  product_id INTEGER REFERENCES products(id), qty INTEGER);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?,?,?)", CUSTOMERS)
    con.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?)", PRODUCTS)
    con.executemany("INSERT INTO orders VALUES (?,?,?,?)", ORDERS)
    con.executemany("INSERT INTO order_items VALUES (?,?,?)", ORDER_ITEMS)
    con.commit()
    con.close()
    return path


if __name__ == "__main__":
    print(f"Created {build()}")
