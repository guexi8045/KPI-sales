<script lang="ts">
  import { onMount } from "svelte";

  type Row = {
    id: number | string;
    month: string; // Abschluss-Monat (YYYY-MM)
    abschlussdatum: string; // YYYY-MM-DD
    eintrittsdatum: string; // YYYY-MM-DD
    anzahl_tage: number;
  };

  let rows: Row[] = [];
  let loading = true;
  let error: string | null = null;

  let grouped: Record<string, Row[]> = {};
  let months: string[] = [];

  function groupByMonth(data: Row[]) {
    const g: Record<string, Row[]> = {};
    for (const r of data) {
      (g[r.month] ||= []).push(r);
    }
    // innerhalb des Monats sortieren
    for (const m of Object.keys(g)) {
      g[m].sort((a, b) =>
        (a.abschlussdatum ?? "").localeCompare(b.abschlussdatum ?? "") ||
        (a.eintrittsdatum ?? "").localeCompare(b.eintrittsdatum ?? "") ||
        String(a.id).localeCompare(String(b.id))
      );
    }
    return g;
  }

  onMount(async () => {
    try {
      const res = await fetch("/api/zeitbiseintritt", { credentials: "include" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      rows = await res.json();

      grouped = groupByMonth(rows);
      months = Object.keys(grouped).sort((a, b) => a.localeCompare(b));
    } catch (e: any) {
      error = e?.message ?? "Fehler beim Laden";
    } finally {
      loading = false;
    }
  });
</script>

<h1>Abschlussmonat → zugehörige Eintrittsdaten</h1>
<p style="margin-top: 0.25rem; opacity: 0.8;">
  Gruppiert nach Abschlussdatum (YYYY-MM). Pro Deal siehst du Abschluss- und Eintrittsdatum.
</p>

{#if loading}
  <p>Lade…</p>
{:else if error}
  <p style="color: red">{error}</p>
{:else if months.length === 0}
  <p>Keine Daten gefunden.</p>
{:else}
  {#each months as m}
    <h2 style="margin-top: 1.5rem;">{m}</h2>

    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th style="text-align:left; padding: 6px; border-bottom: 1px solid #ddd;">Deal ID</th>
          <th style="text-align:left; padding: 6px; border-bottom: 1px solid #ddd;">Abschlussdatum</th>
          <th style="text-align:left; padding: 6px; border-bottom: 1px solid #ddd;">Eintrittsdatum</th>
          <th style="text-align:left; padding: 6px; border-bottom: 1px solid #ddd;">Tage bis Eintritt</th>
        </tr>
      </thead>
      <tbody>
        {#each grouped[m] as r}
          <tr>
            <td style="padding: 6px; border-bottom: 1px solid #f0f0f0;">{r.id}</td>
            <td style="padding: 6px; border-bottom: 1px solid #f0f0f0;">{r.abschlussdatum}</td>
            <td style="padding: 6px; border-bottom: 1px solid #f0f0f0;">{r.eintrittsdatum}</td>
            <td style="padding: 6px; border-bottom: 1px solid #f0f0f0;">{r.anzahl_tage}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/each}
{/if}
