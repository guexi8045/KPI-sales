import pandas as pd
from reports.database import get_connection

def get_zeitbiseintritt():
    query = """
        SELECT 
            id,
            abschlussdatum,
            eintrittsdatum,
            TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
            EXTRACT(DAY FROM eintrittsdatum::timestamp - abschlussdatum::timestamp) AS anzahl_tage
        FROM deals
        WHERE abschlussdatum IS NOT NULL AND eintrittsdatum IS NOT NULL
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    df_grouped = df.groupby('month')['anzahl_tage'].mean().reset_index()
    df_grouped['category_name'] = 'Ø Tage bis Eintritt'
    df_grouped['num_deals'] = df_grouped['anzahl_tage'].round(2)
    return df_grouped[['month', 'category_name', 'num_deals']].to_dict(orient="records")
