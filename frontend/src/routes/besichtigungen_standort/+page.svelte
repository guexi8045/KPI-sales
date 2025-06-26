<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/besichtigungen_standort"
  title="Anzahl Besichtigungen pro Standort"
  valueKey="num_deals"
/>
