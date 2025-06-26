<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/tage_zunahme_standort"
  title="Zunahme Tage pro Standort"
  valueKey="num_deals"
/>
