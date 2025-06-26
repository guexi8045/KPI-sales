<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/tage_zunahme"
  title="Zunahme Tage pro Monat"
  valueKey="num_deals"
/>
