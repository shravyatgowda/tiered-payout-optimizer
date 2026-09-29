"""Generate SYNTHETIC delivery-partner trip data (no real company data)."""
import random, sqlite3, sys
from datetime import date, timedelta

def main(n_trips=20000, n_partners=60, seed=42, db="data/trips.db"):
    import os; os.makedirs(os.path.dirname(db), exist_ok=True)
    random.seed(seed)
    con = sqlite3.connect(db)
    con.executescript(open("sql/schema.sql").read())
    start = date(2025, 1, 6)
    rows = []
    for i in range(n_trips):
        d = start + timedelta(days=random.randint(0, 55))
        dist = round(random.uniform(0.5, 12), 2)
        base = round(15 + dist * 6, 2)          # baseline payout rule
        paid = base
        # inject known data-quality issues so detection can be tested
        r = random.random()
        if r < 0.02:   paid = round(base * 1.5, 2)   # manual override inflating payout
        elif r < 0.03: dist = 0.0                    # zero-distance trip still paid
        rows.append((i + 1, random.randint(1, n_partners), d.isoformat(),
                     dist, base, paid, random.randint(8, 55)))
    con.executemany("INSERT INTO trips VALUES (?,?,?,?,?,?,?)", rows)
    con.commit(); con.close()
    print(f"Wrote {n_trips} synthetic trips to {db}")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20000)
