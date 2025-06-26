<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/kuendigungen_standort"
  title="Anzahl Kündigungen nach Standort exkl. Grund = KIGA (nicht gekündete Tage und auch keine Tagesreduktionen berücksichtigt)"
  valueKey="num_deals"
/>
