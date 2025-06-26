from drop_tables import drop_tables
from init_pg_schema import init_schema
from load_deals_pg import fetch_and_store_deals
from load_mutationen_pg import fetch_mutationen

if __name__ == "__main__":
    drop_tables()
    init_schema()
    fetch_and_store_deals()
    fetch_mutationen()
    print("Tägliche Aktualisierung abgeschlossen.")
