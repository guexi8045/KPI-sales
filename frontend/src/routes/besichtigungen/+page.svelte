<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/besichtigungen"
  title="Anzahl Besichtigungen pro Monat"
  valueKey="num_deals"
/>
