<script lang="ts">
  import { onMount } from "svelte";

  type Row = {
    id: number;
    status?: string;
    abschlussdatum: string;
    eintrittsdatum: string;
    eintritt_month?: string;
    tage_bis_eintritt?: number | null;
    alter_beim_eintritt?: string | null;
    notitzen_subventionen?: string | null;
    anzahl_tage?: number | null;
    besichtigungsstandort?: string | null;
  };

  let selectedMonth = "";
  let rows: Row[] = [];
  let loading = false;
  let error: string | null = null;

  // Optional: Filter (wenn du sie nicht willst, kannst du den Block löschen)
  let filterBaby = true;
  let filterKleinkind = true;
  let filterUnbekannt = true;

  function getCurrentMonth() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    return `${year}-${month}`;
  }

  async function load() {
    if (!selectedMonth) return;

    loading = true;
    error = null;

    try {
      const res = await fetch(`/api/zeitbiseintritt?month=${selectedMonth}`);
      if (!res.ok) throw new Error(await res.text());
      rows = await res.json();
    } catch (e: any) {
      error = e?.message ?? String(e);
      rows = [];
    } finally {
      loading = false;
    }
  }

  function groupByEintrittMonth(items: Row[]) {
    const map = new Map<string, Row[]>();
    for (const r of items) {
      const key = r.eintritt_month ?? "Unbekannt";
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(r);
    }
    return Array.from(map.entries());
  }

  function subventionLabel(v: any) {
    if (!v) return "Nein";
    return "Ja";
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

  function filteredRows() {
    return rows.filter(passAlterFilter);
  }

  onMount(() => {
    selectedMonth = getCurrentMonth();
    load();
  });
</script>

<h1>Zeit bis Eintritt</h1>
<p>
  Wähle einen <strong>Abschlussmonat</strong> und sieh alle <strong>WON</strong>-Abschlüsse inkl. Eintrittsmonat und
  Details. Gruppiert nach Eintrittsmonat.
</p>

<div style="display:flex; gap:12px; align-items:end; margin: 12px 0; flex-wrap: wrap;">
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
    <strong>Anzahl Deals:</strong> {filteredRows().length}
  </p>
{/if}

{#if !loading && filteredRows().length === 0}
  <p>Keine WON-Abschlüsse im gewählten Monat (oder Filter schließt alles aus).</p>
{/if}

{#if filteredRows().length > 0}
  {#each groupByEintrittMonth(filteredRows()) as [eintrittMonth, grp]}
    <h3 style="margin-top:16px;">Eintritt: {eintrittMonth} ({grp.length})</h3>

    <div style="overflow:auto;">
      <table style="width:100%; border-collapse: collapse; min-width: 980px;">
        <thead>
          <tr>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Deal-ID</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Abschluss</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Eintritt</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Tage bis Eintritt</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Alter</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Subvention</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Anzahl Tage</th>
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Standort</th>
          </tr>
        </thead>

        <tbody>
          {#each grp as r}
            <tr>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.id}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.abschlussdatum}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.eintrittsdatum}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.tage_bis_eintritt ?? ""}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">
                {normalizeAlter(r.alter_beim_eintritt)}
              </td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">
                {subventionLabel(r.notitzen_subventionen)}
              </td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.anzahl_tage ?? ""}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">
                {r.besichtigungsstandort ?? ""}
              </td>
            </tr>

            {#if r.notitzen_subventionen}
              <tr>
                <td colspan="8" style="padding:6px; border-bottom:1px solid #f0f0f0; font-size: 0.95em;">
                  <strong>Subventions-Notiz:</strong> {r.notitzen_subventionen}
                </td>
              </tr>
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
  {/each}
{/if}
