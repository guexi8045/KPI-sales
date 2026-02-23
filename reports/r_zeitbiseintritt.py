import pandas as pd
from reports.database import get_connection

def get_zeitbiseintritt(abschluss_month: str):
    """
    abschluss_month: 'YYYY-MM' z.B. '2025-12'
    Liefert Deal-Level Daten für alle WON Abschlüsse im Monat,
    sortiert nach Eintrittsmonat/-datum.
    """
    query = """
        WITH params AS (
            SELECT
                to_date(%s || '-01', 'YYYY-MM-DD') AS month_start,
                (to_date(%s || '-01', 'YYYY-MM-DD') + INTERVAL '1 month') AS month_end
        )
        SELECT
            id,
            status,
            abschlussdatum,
            eintrittsdatum,
            TO_CHAR(date_trunc('month', eintrittsdatum::date), 'YYYY-MM') AS eintritt_month,
            (eintrittsdatum::date - abschlussdatum::date) AS tage_bis_eintritt,
            alter_beim_eintritt,
            notitzen_subventionen,
            anzahl_tage,
            besichtigungsstandort
        FROM deals
        CROSS JOIN params p
        WHERE
            status = 'won'
            AND abschlussdatum IS NOT NULL AND abschlussdatum <> ''
            AND eintrittsdatum IS NOT NULL AND eintrittsdatum <> ''
            AND abschlussdatum::date >= p.month_start
            AND abschlussdatum::date < p.month_end
        ORDER BY
            eintritt_month ASC,
            eintrittsdatum::date ASC,
            abschlussdatum::date ASC;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=[abschluss_month, abschluss_month])
    conn.close()

    if "tage_bis_eintritt" in df.columns:
        df["tage_bis_eintritt"] = df["tage_bis_eintritt"].astype("Int64")

    return df.to_dict(orient="records")
