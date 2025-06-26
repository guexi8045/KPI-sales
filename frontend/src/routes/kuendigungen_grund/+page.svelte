<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/kuendigungsgruende"
  title="Anzahl Kündigungen nach Grund (nicht gekündete Tage und auch keine Tagesreduktionen berücksichtigt)"
  valueKey="num_deals"
/>
