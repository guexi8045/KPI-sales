<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/tage_abnahme_standort"
  title="Abnahme Tage pro Standort. Kündigungen und Mutationen berücksichtigt. Exkl. Grund = KIGA"
  valueKey="num_deals"
/>
