"""Back-test candidate weekly incentive tier structures on historical trips."""
import sqlite3, csv, os

# (min_weekly_trips, bonus_per_trip) - highest matching tier applies
STRUCTURES = {
    "current":   [(0, 0.0), (35, 2.0), (45, 4.0)],
    "steeper":   [(0, 0.0), (35, 2.5), (45, 5.5)],
    "wider":     [(0, 0.0), (25, 1.5), (40, 3.0), (50, 5.0)],
}

def bonus(trips, tiers):
    rate = 0.0
    for min_trips, r in tiers:
        if trips >= min_trips:
            rate = r
    return trips * rate

def main(db="data/trips.db"):
    con = sqlite3.connect(db)
    print("== Data-quality edge cases ==")
    for row in con.execute(open("sql/anomalies.sql").read()):
        print(f"{row[0]:<20} trips={row[1]:<6} excess=Rs {row[2]}")
    weekly = con.execute(open("sql/weekly_partner.sql").read()).fetchall()
    os.makedirs("output", exist_ok=True)
    out = []
    print("\n== Tier back-test (total incentive cost) ==")
    for name, tiers in STRUCTURES.items():
        total = sum(bonus(t, tiers) for _, _, t, _ in weekly)
        paid_weeks = sum(1 for _, _, t, _ in weekly if bonus(t, tiers) > 0)
        out.append((name, round(total, 2), paid_weeks))
        print(f"{name:<8} cost=Rs {total:,.0f}  partner-weeks earning bonus={paid_weeks}")
    with open("output/backtest_summary.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["structure", "total_incentive", "partner_weeks_paid"]); w.writerows(out)

if __name__ == "__main__":
    main()
