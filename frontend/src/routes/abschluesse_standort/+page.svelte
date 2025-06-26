<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/abschluesse_standort"
  title="Anzahl Abschlüsse nach Standort"
  valueKey="num_deals"
/>
