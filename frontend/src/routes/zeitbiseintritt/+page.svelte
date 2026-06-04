<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  type Row = {
    typ: "EINTRITT" | "MUTATION+" | "MUTATION-" | "KÜNDIGUNG";
    id: number;
    datum: string;
    abschlussdatum?: string | null;
    tage_bis_eintritt?: number | null;
    alter?: string | null;
    finanzierung?: string | null;
    standort?: string | null;
    tage?: number | null;
    kuendigungsgrund?: string | null;
  };

  type Summary = {
    zuwachs_tage: number;
    abnahme_tage: number;
    netto_tage: number;
    zuwachs_plaetze: number;
    abnahme_plaetze: number;
    netto_plaetze: number;
  };

  let selectedMonth = "";
  let rows: Row[] = [];
  let summary: Summary | null = null;

  let loading = false;
  let error: string | null = null;

  let showZuwachs = true;
  let showAbnahme = true;
  let showNetto = false;

  function getCurrentMonth() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    return `${year}-${month}`;
  }

  function plaetzeFromTage(v: any) {
    const n = Number(v);
    if (!Number.isFinite(n) || n === 0) return "";
    const p = n / 5;
    return p % 1 === 0 ? String(p) : p.toFixed(1);
  }

  function isZuwachs(r: Row) {
    return r.typ === "EINTRITT" || r.typ === "MUTATION+";
  }

  function isAbnahme(r: Row) {
    return r.typ === "KÜNDIGUNG" || r.typ === "MUTATION-";
  }

  $: filtered = rows.filter((r) => {
    if (showNetto) return true;
    return (showZuwachs && isZuwachs(r)) || (showAbnahme && isAbnahme(r));
  });

  function typLabel(t: Row["typ"]) {
    if (t === "EINTRITT") return "Eintritt";
    if (t === "MUTATION+") return "Mutation +";
    if (t === "MUTATION-") return "Mutation -";
    return "Kündigung";
  }

  function fmtFinanzierung(v: any) {
    const s = (v ?? "").toString().trim();
    return s || "—";
  }

  async function load() {
    if (!selectedMonth) return;

    loading = true;
    error = null;

    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`/api/zeitbiseintritt?month=${selectedMonth}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.status === 401) {
        alert("Session abgelaufen. Bitte erneut einloggen.");
        localStorage.removeItem("token");
        goto("/login");
        return;
      }

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `HTTP ${res.status}`);
      }

      const data = await res.json();

      rows = Array.isArray(data?.rows) ? data.rows : [];
      summary = data?.summary ?? null;

    } catch (e: any) {
      error = e?.message ?? String(e);
      rows = [];
      summary = null;
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    selectedMonth = getCurrentMonth();
    load();
  });
</script>

<style>

.controls {
  display: flex;
  gap: 12px;
  align-items: end;
  margin: 12px 0;
  flex-wrap: wrap;
}

.tableWrap {
  overflow: auto;
}

.summaryBox {
  margin: 10px 0 14px 0;
  padding: 10px 12px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  background: #fafafa;
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  align-items: center;
}

.summaryItem b {
  display: inline-block;
  min-width: 70px;
}

table.report {
  width: 100%;
  border-collapse: collapse;
  min-width: 1080px;
  table-layout: fixed;
}

table.report th,
table.report td {
  border-bottom: 1px solid #f0f0f0;
  padding: 8px;
  vertical-align: middle;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

table.report th {
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.center-num {
  text-align: center;
  font-variant-numeric: tabular-nums;
}

.link {
  color: #007acc;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

</style>

<h1>Zeit bis Eintritt</h1>

<p>
  Wähle einen <strong>Monat</strong> und sieh eine gemeinsame Liste aus
  <strong>Eintritten</strong>, <strong>Mutationen</strong> und
  <strong>Kündigungen</strong>.
</p>

<div class="controls">

<label>
  Monat:
  <input type="month" bind:value={selectedMonth} />
</label>

<button on:click={load} disabled={loading || !selectedMonth}>
  {loading ? "Lade…" : "Anzeigen"}
</button>

<div style="display:flex; gap:12px; align-items:center;">
  <label>
    <input type="checkbox" bind:checked={showZuwachs} disabled={showNetto}>
    Zuwachs
  </label>

  <label>
    <input type="checkbox" bind:checked={showAbnahme} disabled={showNetto}>
    Abnahme
  </label>

  <label>
    <input type="checkbox" bind:checked={showNetto}>
    Netto
  </label>
</div>

</div>

{#if error}
<p style="color:red; white-space: pre-wrap;">{error}</p>
{/if}

{#if summary}

<div class="summaryBox">

<div class="summaryItem">
<b>Zuwachs:</b>
{summary.zuwachs_tage} Tage
({plaetzeFromTage(summary.zuwachs_tage)} Plätze)
</div>

<div class="summaryItem">
<b>Abnahme:</b>
{summary.abnahme_tage} Tage
({plaetzeFromTage(summary.abnahme_tage)} Plätze)
</div>

<div class="summaryItem">
<b>Netto:</b>
{summary.netto_tage} Tage
({plaetzeFromTage(summary.netto_tage)} Plätze)
</div>

</div>

{/if}

{#if !loading}
<p style="margin: 8px 0;">
<strong>Anzahl Zeilen:</strong> {filtered.length}
</p>
{/if}

{#if !loading && filtered.length === 0}
<p>Keine Einträge im gewählten Monat.</p>
{/if}

{#if filtered.length > 0}

<div class="tableWrap">

<table class="report">

<thead>
<tr>
<th style="width:110px;">Typ</th>
<th style="width:90px;">Deal-ID</th>
<th style="width:130px;">Datum</th>
<th style="width:130px;">Abschluss</th>
<th style="width:140px; text-align:center;">Tage bis Eintritt</th>
<th style="width:120px;">Alter</th>
<th style="width:140px;">Finanzierung</th>
<th style="width:120px; text-align:center;">Tage (+/-)</th>
<th style="width:90px; text-align:center;">Plätze</th>
<th style="width:180px;">Standort</th>
<th style="width:160px;">Kündigungsgrund</th>
</tr>
</thead>

<tbody>

{#each filtered as r}

<tr>

<td>{typLabel(r.typ)}</td>

<td>
<a
class="link"
href={`https://guexi.pipedrive.com/deal/${r.id}`}
target="_blank"
rel="noopener noreferrer"
>
{r.id}
</a>
</td>

<td>{r.datum ?? ""}</td>
<td>{r.abschlussdatum ?? "—"}</td>

<td class="center-num">
{r.tage_bis_eintritt ?? "—"}
</td>

<td>{r.alter ?? "—"}</td>

<td>{fmtFinanzierung(r.finanzierung)}</td>

<td class="center-num">
{r.tage ?? "—"}
</td>

<td class="center-num">
{plaetzeFromTage(r.tage)}
</td>

<td>{r.standort ?? "—"}</td>

<td>{r.kuendigungsgrund ?? "—"}</td>

</tr>

{/each}

</tbody>

</table>

</div>

{/if}
