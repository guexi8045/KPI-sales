<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/abschluesse_finanzierung"
  title="Anzahl abgeschlossene Tage nach Finanzierung."
  valueKey="total_days"
/>
