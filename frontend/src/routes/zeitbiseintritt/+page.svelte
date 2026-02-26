<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  type Row = {
    id: number;
    status?: string;
    abschlussdatum: string;
    eintrittsdatum: string;
    eintritt_month?: string | null;
    tage_bis_eintritt?: number | null;
    alter_beim_eintritt?: string | null;
    finanzierung?: string | null;
    anzahl_tage?: number | null;
    besichtigungsstandort?: string | null;
  };

  let selectedMonth = "";
  let rows: Row[] = [];
  let loading = false;
  let error: string | null = null;

  let filterBaby = true;
  let filterKleinkind = true;
  let filterUnbekannt = true;

  function getCurrentMonth() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    return `${year}-${month}`;
  }

  function normalizeAlter(v: any) {
    const s = (v ?? "").toString().trim();
    if (!s) return "Unbekannt";
    return s;
  }

  function passAlterFilter(r: Row) {
    const a = normalizeAlter(r.alter_beim_eintritt).toLowerCase();
    const isBaby = a.includes("baby");
    const isKleinkind = a.includes("kleinkind");
    const isUnbekannt = !isBaby && !isKleinkind;

    return (
      (filterBaby && isBaby) ||
      (filterKleinkind && isKleinkind) ||
      (filterUnbekannt && isUnbekannt)
    );
  }

  $: filtered = rows.filter(passAlterFilter);

  function getEintrittMonth(r: Row) {
    const m = (r.eintritt_month ?? "").toString().trim();
    return m ? m : "Unbekannt";
  }

  function groupByEintrittMonth(items: Row[]) {
    const map = new Map<string, Row[]>();
    for (const r of items) {
      const key = getEintrittMonth(r);
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(r);
    }
    return Array.from(map.entries()).sort((a, b) => a[0].localeCompare(b[0]));
  }

  $: groups = groupByEintrittMonth(filtered);

  function finanzierungLabel(v: any) {
    const s = (v ?? "").toString().trim();
    if (!s) return "Unbekannt";
    return s;
  }

  function plaetze(v: any) {
    const n = Number(v);
    if (!Number.isFinite(n) || n <= 0) return "";
    const p = n / 5;
    return p % 1 === 0 ? String(p) : p.toFixed(1);
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
      rows = Array.isArray(data) ? data : [];
    } catch (e: any) {
      error = e?.message ?? String(e);
      rows = [];
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

  table.report {
    width: 100%;
    border-collapse: collapse;
    min-width: 980px;
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

  /* ✅ Zahlen mittig */
  .center-num {
    text-align: center;
    font-variant-numeric: tabular-nums;
  }
</style>

<h1>Zeit bis Eintritt</h1>
<p>
  Wähle einen <strong>Abschlussmonat</strong> und sieh alle <strong>WON</strong>-Abschlüsse inkl.
  Eintrittsmonat und Details. Gruppiert nach Eintrittsmonat.
</p>

<div class="controls">
  <label>
    Abschlussmonat:
    <input type="month" bind:value={selectedMonth} />
  </label>

  <button on:click={load} disabled={loading || !selectedMonth}>
    {loading ? "Lade…" : "Anzeigen"}
  </button>

  <div style="display:flex; gap:12px; align-items:center;">
    <label><input type="checkbox" bind:checked={filterBaby} /> Baby</label>
    <label><input type="checkbox" bind:checked={filterKleinkind} /> Kleinkind</label>
    <label><input type="checkbox" bind:checked={filterUnbekannt} /> Unbekannt</label>
  </div>
</div>

{#if error}
  <p style="color:red; white-space: pre-wrap;">{error}</p>
{/if}

{#if !loading}
  <p style="margin: 8px 0;">
    <strong>Anzahl Deals:</strong> {filtered.length}
  </p>
{/if}

{#if !loading && filtered.length === 0}
  <p>Keine WON-Abschlüsse im gewählten Monat (oder Filter schließt alles aus).</p>
{/if}

{#if filtered.length > 0}
  {#each groups as [eintrittMonth, grp]}
    <h3 style="margin-top:16px;">Eintritt: {eintrittMonth} ({grp.length})</h3>

    <div class="tableWrap">
      <table class="report">
        <thead>
          <tr>
            <th style="width: 90px;">Deal-ID</th>
            <th style="width: 120px;">Abschluss</th>
            <th style="width: 120px;">Eintritt</th>
            <th style="width: 120px; text-align:center;">Tage bis Eintritt</th>
            <th style="width: 120px;">Alter</th>
            <th style="width: 140px;">Finanzierung</th>
            <th style="width: 90px; text-align:center;">Plätze</th>
            <th style="width: 160px;">Standort</th>
          </tr>
        </thead>

        <tbody>
          {#each grp as r}
            <tr>
              <td>{r.id}</td>
              <td>{r.abschlussdatum}</td>
              <td>{r.eintrittsdatum}</td>
              <td class="center-num">{r.tage_bis_eintritt ?? ""}</td>
              <td>{normalizeAlter(r.alter_beim_eintritt)}</td>
              <td>{finanzierungLabel(r.finanzierung)}</td>
              <td class="center-num">{plaetze(r.anzahl_tage)}</td>
              <td>{r.besichtigungsstandort ?? ""}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/each}
{/if}
