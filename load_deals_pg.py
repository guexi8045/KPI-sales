import requests
import os
from dotenv import load_dotenv
from reports.database import get_connection

load_dotenv()

api_token = os.getenv("PIPEDRIVE_API_TOKEN") or 'DEIN_API_TOKEN_HIER'
pipeline_ids = [1, 37]
limit = 500

STANDORT_MAPPING = {
    '199': 'Friesenberg', '200': 'Lindenplatz', '201': 'Sonnenberg', '202': 'Schwamendingen Post',
    '203': 'Schwamendingen Dubi', '204': 'Richterswil Dorf', '205': 'Richterswil Boden', '206': 'B414',
    '207': 'B288', '208': 'H2', '209': 'N7', '210': 'Z60', '211': 'Z53', '298': 'Uster'
}

ABSAGEGRUND_MAPPING = {
    '212': 'Weg', '213': 'Andere Kita besser', '214': 'Wunschtage nicht verfugbar',
    '215': 'Andere Betreuungslosung', '216': 'Unsicher', '217': 'Kosten', '218': 'Umzug', '219': 'Sonstiges'
}

ANZAHL_TAGE_MAPPING = {
    '224': 5, '223': 4, '222': 3, '221': 2, '220': 1
}

KANAL_MAPPING = {
    '158': 'Email', '159': 'Kontaktformular', '160': 'Telefon', '161': 'Bestandskunde', '162': 'Sonstiges'
}

EMPFEHLUNG_MAPPING = {
    '230': 'nein', '229': 'ja'
}

HERKUNFT_MAPPING = {
    '163': 'Empfehlung', '164': 'Google Ads', '165': 'Google SEO', '166': 'Google unklar',
    '167': 'Google Maps', '168': 'Facebook', '169': 'Instagram', '170': 'Tiktok', '171': 'Flyer',
    '172': 'Schaufenster', '173': 'Kita unterwegs', '174': 'Empfehlung von Amt', '175': 'GVK',
    '176': 'Stadt Zuerich Krippenuebersicht', '177': 'Sonstiges', '178': 'Bestandskunde'
}

FINANZIERUNG_MAPPING = {
    '228': 'Subventioniert', '227': 'Privat'
}

ALTER_MAPPING = {
    '226': 'Kleinkind', '225': 'Baby'
}

KRIPPENLEITUNG_MAPPING = {
    '179': 'Preetha', '180': 'Friesenberg Baby', '181': 'Friesenberg KK', '182': 'Friesenberg Wald',
    '183': 'Arjeta', '184': 'Lindenplatz Baby', '185': 'Lindenplatz KK', '186': 'Lindenplatz Wald',
    '187': 'Sonnenberg', '188': 'Schwamendingen Post Wald', '189': 'Schwamendingen Post KK',
    '190': 'Schwamedingen Dubi', '191': 'Richterswil Dorf', '192': 'Richterswil Boden', '193': 'B414',
    '194': 'B288', '195': 'H2', '196': 'N7', '197': 'Z60', '198': 'Z53', '300': 'Uster',
    '301': 'Ellen', '302': 'Keine Besichtigung'
}

field_ids = {
    'ID': 'id', 'Status': 'status', 'Empfehlung?': 'acffba9f706b8dbc738681c8ced64d1afbd9cf77',
    'Finanzierung': '29bdc22200824f43406fa66bbab17b33e2d64fd3',
    'Alter beim Eintritt': '802324f78262562d86d9e5f58b5554a7d9dd4ba3',
    'Anzahl Tage': '4f3fa7fc26f78fe6cece991b8f0aeb77188a4f28',
    'Absagegrund': '8a632087ef0a31d8a54c8b3d88dea6bcaf98870b',
    'Besichtigungsstandort': '3f97b3e113f6cca89ec3b0f6a1b5711628ca27d5',
    'Krippenleitung': '56fd566a8fa46e4f9e3321fc713a9fc0578df7f0',
    'Abschlussdatum': 'a9aadf14a6804f6452a1b499ba1aab82b429d82a',
    'Besichtigungsdatum': 'a6ac52c28710d2aa1c002f650cf2c4e2b0416649',
    'Herkunft': '66a298d3af94a6230bceb113aa27759a51c37d52',
    'Kanal': '61c70c03d45d17ad594ba78ad0ef96dafcdcf31e',
    'Anfragedatum': '8d944b87da8c56e613390879ca223d31c76e20cb',
    'Notitzen Subventionen': 'd5697dfa4b944f8ab616d59ebff64b0decc9a7ba',
    'Eintrittsdatum': '2645b9369b1b0f46b0821c1eeb77d05c0ffa74d2',
    'Absagedatum': 'ddf65a8017f58dda05bf05fe717c714bc11d3644'
}

def insert_into_postgres(deals):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO deals (
            id, status, empfehlung, finanzierung, alter_beim_eintritt, anzahl_tage,
            absagegrund, besichtigungsstandort, krippenleitung, abschlussdatum, besichtigungsdatum,
            herkunft, kanal, anfragedatum, notitzen_subventionen, absagedatum, eintrittsdatum
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            status = EXCLUDED.status,
            empfehlung = EXCLUDED.empfehlung,
            finanzierung = EXCLUDED.finanzierung,
            alter_beim_eintritt = EXCLUDED.alter_beim_eintritt,
            anzahl_tage = EXCLUDED.anzahl_tage,
            absagegrund = EXCLUDED.absagegrund,
            besichtigungsstandort = EXCLUDED.besichtigungsstandort,
            krippenleitung = EXCLUDED.krippenleitung,
            abschlussdatum = EXCLUDED.abschlussdatum,
            besichtigungsdatum = EXCLUDED.besichtigungsdatum,
            herkunft = EXCLUDED.herkunft,
            kanal = EXCLUDED.kanal,
            anfragedatum = EXCLUDED.anfragedatum,
            notitzen_subventionen = EXCLUDED.notitzen_subventionen,
            absagedatum = EXCLUDED.absagedatum,
            eintrittsdatum = EXCLUDED.eintrittsdatum;
    """

    cursor.executemany(insert_query, deals)
    conn.commit()
    conn.close()

def fetch_and_store_deals():
    for pipeline_id in pipeline_ids:
        print(f"Lade Deals für Pipeline {pipeline_id}")
        page = 0

        while True:
            url = f"https://api.pipedrive.com/v1/deals?api_token={api_token}&pipeline_id={pipeline_id}&start={page * limit}&limit={limit}"
            response = requests.get(url)
            deals = response.json()

            if 'data' not in deals or deals['data'] is None:
                print("Keine Deals gefunden.")
                break

            relevant_deals = [
                deal for deal in deals['data']
                if deal.get(field_ids['Anfragedatum']) is not None
            ]

            insert_data = []
            for deal in relevant_deals:
                try:
                    row = (
                        deal['id'],
                        deal.get('status'),
                        EMPFEHLUNG_MAPPING.get(str(deal.get(field_ids['Empfehlung?'])), 'Unbekannt'),
                        FINANZIERUNG_MAPPING.get(str(deal.get(field_ids['Finanzierung'])), 'Unbekannt'),
                        ALTER_MAPPING.get(str(deal.get(field_ids['Alter beim Eintritt'])), None),
                        ANZAHL_TAGE_MAPPING.get(str(deal.get(field_ids['Anzahl Tage'])), None),
                        ABSAGEGRUND_MAPPING.get(str(deal.get(field_ids['Absagegrund'])), deal.get(field_ids['Absagegrund']) or 'Unbekannt'),
                        STANDORT_MAPPING.get(str(deal.get(field_ids['Besichtigungsstandort'])), 'Unbekannt'),
                        KRIPPENLEITUNG_MAPPING.get(str(deal.get(field_ids['Krippenleitung'])), 'Unbekannt'),
                        deal.get(field_ids['Abschlussdatum']),
                        deal.get(field_ids['Besichtigungsdatum']),
                        HERKUNFT_MAPPING.get(str(deal.get(field_ids['Herkunft'])), 'Unbekannt'),
                        KANAL_MAPPING.get(str(deal.get(field_ids['Kanal'])), 'Unbekannt'),
                        deal.get(field_ids['Anfragedatum']),
                        deal.get(field_ids['Notitzen Subventionen']),
                        deal.get(field_ids['Absagedatum']),
                        deal.get(field_ids['Eintrittsdatum']),
                    )
                    insert_data.append(row)
                except KeyError as e:
                    print(f"Fehler beim Deal: {e}")
                    continue

            if insert_data:
                insert_into_postgres(insert_data)
                print(f"Seite {page} gespeichert ({len(insert_data)} Deals)")
            else:
                print(f"Seite {page} leer")

            if not deals.get('additional_data', {}).get('pagination', {}).get('more_items_in_collection'):
                print(f"Fertig mit Pipeline {pipeline_id}")
                break
            page += 1

if __name__ == "__main__":
    fetch_and_store_deals()
    print("Alle Daten gespeichert.")
