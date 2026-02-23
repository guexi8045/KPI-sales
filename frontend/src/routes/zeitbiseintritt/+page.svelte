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

    // ✅ neu: kommt aus deals.finanzierung (Subventioniert/Privat/noch unklar/Unbekannt)
    finanzierung?: string | null;

    anzahl_tage?: number | null;
    besichtigungsstandort?: string | null;

    // optional behalten falls du es später brauchst
    notitzen_subventionen?: string | null;
  };

  let selectedMonth = "";
  let rows: Row[] = [];
  let loading = false;
  let error: string | null = null;

  // Filter
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

  // reaktiv gefilterte Zeilen
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

  // reaktiv gruppiert
  $: groups = groupByEintrittMonth(filtered);

  // ✅ FIX: Subvention anhand finanzierung korrekt anzeigen
  // Erwartete Werte: "Subventioniert", "Privat", "noch unklar", "(Keine)", "Unbekannt" etc.
  function subventionLabel(v: any) {
    const s = (v ?? "").toString().trim();

    if (!s) return "Unbekannt";

    const lower = s.toLowerCase();
    if (lower === "(keine)" || lower === "keine") return "Unbekannt";
    if (lower.includes("subvention")) return "Subventioniert";
    if (lower.includes("privat")) return "Privat";
    if (lower.includes("unklar")) return "Noch unklar";
    if (lower.includes("unbekannt")) return "Unbekannt";

    // fallback: Original anzeigen
    return s;
  }

  async function load() {
    if (!selectedMonth) return;

    loading = true;
    error = null;

    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`/api/zeitbiseintritt?month=${selectedMonth}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
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
    <strong>Anzahl Deals:</strong> {filtered.length}
  </p>
{/if}

{#if !loading && filtered.length === 0}
  <p>Keine WON-Abschlüsse im gewählten Monat (oder Filter schließt alles aus).</p>
{/if}

{#if filtered.length > 0}
  {#each groups as [eintrittMonth, grp]}
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
            <th style="text-align:left; border-bottom:1px solid #ddd; padding:6px;">Finanzierung</th>
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
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{normalizeAlter(r.alter_beim_eintritt)}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">
                {subventionLabel(r.finanzierung)}
              </td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.anzahl_tage ?? ""}</td>
              <td style="border-bottom:1px solid #f0f0f0; padding:6px;">{r.besichtigungsstandort ?? ""}</td>
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
