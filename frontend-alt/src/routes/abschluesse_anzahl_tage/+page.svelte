<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/abschluesse_anzahl_tage"
  title="Anzahl Abschlüsse nach Anzahl Tage"
  valueKey="num_deals"
/>
