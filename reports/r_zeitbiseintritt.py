import pandas as pd
from reports.database import get_connection

def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.where(pd.notnull(df), None)

def get_zeitbiseintritt(monat: str):
    conn = get_connection()

    # --- Eintritte (deals) nach Eintrittsdatum im Monat ---
    q_deals = """
      WITH params AS (
        SELECT
          to_date(%s || '-01', 'YYYY-MM-DD') AS month_start,
          (to_date(%s || '-01', 'YYYY-MM-DD') + INTERVAL '1 month') AS month_end
      )
      SELECT
        id,
        abschlussdatum,
        eintrittsdatum,
        (eintrittsdatum::date - abschlussdatum::date) AS tage_bis_eintritt,
        alter_beim_eintritt,
        finanzierung,
        anzahl_tage,
        besichtigungsstandort
      FROM deals
      CROSS JOIN params p
      WHERE
        status = 'won'
        AND eintrittsdatum IS NOT NULL AND eintrittsdatum <> ''
        AND abschlussdatum IS NOT NULL AND abschlussdatum <> ''
        AND eintrittsdatum ~ '^\\d{4}-\\d{2}-\\d{2}$'
        AND abschlussdatum ~ '^\\d{4}-\\d{2}-\\d{2}$'
        AND eintrittsdatum::date >= p.month_start
        AND eintrittsdatum::date < p.month_end
      ORDER BY abschlussdatum::date ASC, eintrittsdatum::date ASC
    """
    df_deals = pd.read_sql_query(q_deals, conn, params=(monat, monat))
    df_deals = _clean_df(df_deals)

    # --- Mutationen/Kündigungen nach Wirksamkeitsdatum (= mutationen.abschlussdatum) im Monat ---
    q_mut = """
      WITH params AS (
        SELECT
          to_date(%s || '-01', 'YYYY-MM-DD') AS month_start,
          (to_date(%s || '-01', 'YYYY-MM-DD') + INTERVAL '1 month') AS month_end
      )
      SELECT
        id,
        standort,
        abschlussdatum AS wirksamkeitsdatum,
        mutation_tage_plus_minus,
        kuendigungen_anzahl_tage,
        kuendigungsgrund
      FROM mutationen
      CROSS JOIN params p
      WHERE
        abschlussdatum IS NOT NULL
        AND abschlussdatum <> ''
        AND abschlussdatum ~ '^\\d{4}-\\d{2}-\\d{2}$'
        AND abschlussdatum::date >= p.month_start
        AND abschlussdatum::date < p.month_end
      ORDER BY abschlussdatum::date ASC, id ASC
    """
    df_mut = pd.read_sql_query(q_mut, conn, params=(monat, monat))
    df_mut = _clean_df(df_mut)

    conn.close()

    rows = []

    # EINTRITTE
    for r in df_deals.to_dict(orient="records"):
        rows.append({
            "typ": "EINTRITT",
            "id": r.get("id"),
            "datum": r.get("eintrittsdatum"),
            "abschlussdatum": r.get("abschlussdatum"),
            "standort": r.get("besichtigungsstandort"),
            "alter": r.get("alter_beim_eintritt"),
            "finanzierung": r.get("finanzierung"),
            "tage": r.get("anzahl_tage"),
            "tage_bis_eintritt": r.get("tage_bis_eintritt"),
            "kuendigungsgrund": None
        })

    # MUTATIONEN +/- und KÜNDIGUNGEN
    for r in df_mut.to_dict(orient="records"):
        m = float(r.get("mutation_tage_plus_minus") or 0)
        k = float(r.get("kuendigungen_anzahl_tage") or 0)
        grund = (r.get("kuendigungsgrund") or "").strip()

        if m != 0:
            rows.append({
                "typ": "MUTATION+" if m > 0 else "MUTATION-",
                "id": r.get("id"),
                "datum": r.get("wirksamkeitsdatum"),
                "abschlussdatum": None,
                "standort": r.get("standort"),
                "alter": None,
                "finanzierung": None,
                "tage": m,
                "tage_bis_eintritt": None,
                "kuendigungsgrund": None
            })

        if k < 0 and grund.lower() != "kiga":
            rows.append({
                "typ": "KÜNDIGUNG",
                "id": r.get("id"),
                "datum": r.get("wirksamkeitsdatum"),
                "abschlussdatum": None,
                "standort": r.get("standort"),
                "alter": None,
                "finanzierung": None,
                "tage": k,  # negativ
                "tage_bis_eintritt": None,
                "kuendigungsgrund": grund
            })

    # Sortierung: Datum -> Typ -> ID
    def _sort_key(x):
        return (x.get("datum") or "", x.get("typ") or "", int(x.get("id") or 0))
    rows.sort(key=_sort_key)

    # Summary
    def _sum_types(types: set[str]) -> float:
        return sum(float(r.get("tage") or 0) for r in rows if r.get("typ") in types)

    eintritte = _sum_types({"EINTRITT"})
    mut_plus  = _sum_types({"MUTATION+"})
    mut_minus = _sum_types({"MUTATION-"})
    kuend     = _sum_types({"KÜNDIGUNG"})

    zuwachs = eintritte + mut_plus
    abnahme = kuend + mut_minus  # negativ
    netto   = zuwachs + abnahme

    def _plaetze(t: float) -> float:
        return t / 5.0

    return {
        "month": monat,
        "rows": rows,
        "summary": {
            "zuwachs_tage": zuwachs,
            "abnahme_tage": abnahme,
            "netto_tage": netto,
            "zuwachs_plaetze": _plaetze(zuwachs),
            "abnahme_plaetze": _plaetze(abnahme),
            "netto_plaetze": _plaetze(netto),
        }
    }
