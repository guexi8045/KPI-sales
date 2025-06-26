<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/abschluesse_alter"
  title="Anzahl abgeschlossene Tage nach Alter"
  valueKey="total_days"
/>
