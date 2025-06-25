<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/abschluesse_herkunft"
  title="Anzahl Abschlüsse nach Herkunft"
  valueKey="num_deals"
/>
