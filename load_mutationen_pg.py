import requests
import os
from dotenv import load_dotenv
from reports.database import get_connection

load_dotenv()

api_token = os.getenv("PIPEDRIVE_API_TOKEN")
pipeline_ids = [1, 37]
limit = 500

field_ids = {
    'id': 'id',
    'kuendigungen_anzahl_tage': 'c481e6c8e0d7143d09be07e0a719361e94ea79c8',
    'mutation_tage_plus_minus': 'd918148f89208401b02ea7d67bb7fad70cdb6a9d',
    'abschlussdatum': 'c2dfe366fc88e28a0788e8b7821b7ac69723202f',
    'kuendigungsgrund': 'b5fbbe29ec39e2b57b3fca819a64bbec36548ad3',
    'standort': '4a0c7a697033203c2d84eb66ad8d6dec372e438b'
}

KUENDIGUNG_TAGE_MAPPING = {
    '239': -1, '240': -2, '241': -3, '242': -4, '243': -5
}

MUTATION_TAGE_MAPPING = {
    '231': 1, '232': 2, '233': 3, '234': 4, '235': -1, '236': -2, '237': -3, '238': -4
}

KUENDIGUNGSGRUND_MAPPING = {
    '244': 'KIGA', '245': 'Wegzug', '246': 'Andere Kita', '247': 'Unzufrieden', '248': 'Finanziell', '249': 'Sonstiges'
}

STANDORT_MAPPING = {
    '250': 'Friesenberg', '251': 'Lindenplatz', '252': 'Sonnenberg', '253': 'Schwamendingen Post',
    '254': 'Schwamendingen Dubi', '255': 'Richterswil Dorf', '256': 'Richterswil Boden',
    '257': 'B414', '258': 'B288', '259': 'H2', '260': 'N7', '261': 'Z60', '262': 'Z53', '299': 'Uster'
}

def insert_into_postgres(records):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO mutationen (
            id, kuendigungen_anzahl_tage, mutation_tage_plus_minus,
            abschlussdatum, kuendigungsgrund, standort
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            kuendigungen_anzahl_tage = EXCLUDED.kuendigungen_anzahl_tage,
            mutation_tage_plus_minus = EXCLUDED.mutation_tage_plus_minus,
            abschlussdatum = EXCLUDED.abschlussdatum,
            kuendigungsgrund = EXCLUDED.kuendigungsgrund,
            standort = EXCLUDED.standort;
    """, records)
    conn.commit()
    conn.close()

def fetch_mutationen():
    for pipeline_id in pipeline_ids:
        print(f"Lade Mutationen aus Pipeline {pipeline_id}")
        page = 0

        while True:
            url = f"https://api.pipedrive.com/v1/deals?api_token={api_token}&pipeline_id={pipeline_id}&start={page * limit}&limit={limit}"
            response = requests.get(url)
            deals = response.json()

            if 'data' not in deals or deals['data'] is None:
                print("Keine Deals gefunden.")
                break

            insert_data = []
            for deal in deals['data']:
                if deal.get(field_ids['abschlussdatum']) is None:
                    continue
                try:
                    kuendig_tage = KUENDIGUNG_TAGE_MAPPING.get(str(deal.get(field_ids['kuendigungen_anzahl_tage'])), 0)
                    mutation_tage = MUTATION_TAGE_MAPPING.get(str(deal.get(field_ids['mutation_tage_plus_minus'])), 0)
                    grund = KUENDIGUNGSGRUND_MAPPING.get(str(deal.get(field_ids['kuendigungsgrund'])), 'Unbekannt')
                    standort = STANDORT_MAPPING.get(str(deal.get(field_ids['standort'])), 'Unbekannt')

                    insert_data.append((
                        deal['id'],
                        kuendig_tage,
                        mutation_tage,
                        deal.get(field_ids['abschlussdatum']),
                        grund,
                        standort,
                    ))
                except KeyError as e:
                    print(f"Fehler: {e}")
                    continue

            if insert_data:
                insert_into_postgres(insert_data)
                print(f"Seite {page} gespeichert ({len(insert_data)} Einträge)")
            else:
                print(f"Seite {page} leer")

            if not deals.get('additional_data', {}).get('pagination', {}).get('more_items_in_collection'):
                print(f"Fertig mit Pipeline {pipeline_id}")
                break

            page += 1

if __name__ == "__main__":
    fetch_mutationen()
    print("Mutationen erfolgreich gespeichert.")
