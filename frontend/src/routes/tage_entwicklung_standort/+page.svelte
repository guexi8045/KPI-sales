<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/tage_entwicklung_standort"
  title="Tage Entwicklung (Zunahme-Abnahme) pro Standort. Mutationen, Neukunden und Kündigungen berücksichtigt. Exkl. Grund = KIGA"
  valueKey="num_deals"
/>
