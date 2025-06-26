<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/abschluesse_anzahl_tage"
  title="Anzahl Abschlüsse nach Anzahl Tage"
  valueKey="num_deals"
/>
