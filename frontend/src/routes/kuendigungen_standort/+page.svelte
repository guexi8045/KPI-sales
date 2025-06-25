<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/kuendigungen_standort"
  title="Anzahl Kündigungen nach Standort exkl. Grund = KIGA (nicht gekündete Tage und auch keine Tagesreduktionen berücksichtigt)"
  valueKey="num_deals"
/>
