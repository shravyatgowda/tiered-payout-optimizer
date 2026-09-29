DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
    trip_id        INTEGER PRIMARY KEY,
    partner_id     INTEGER NOT NULL,
    trip_date      TEXT    NOT NULL,
    distance_km    REAL    NOT NULL,
    base_payout    REAL    NOT NULL,  -- expected payout from the standard rule
    paid_payout    REAL    NOT NULL,  -- payout actually recorded
    delivery_min   INTEGER NOT NULL
);
CREATE INDEX idx_trips_partner_date ON trips(partner_id, trip_date);
