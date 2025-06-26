<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/abschluesse_herkunft"
  title="Anzahl Abschlüsse nach Herkunft"
  valueKey="num_deals"
/>
