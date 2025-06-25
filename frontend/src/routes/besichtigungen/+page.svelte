<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/besichtigungen"
  title="Anzahl Besichtigungen pro Monat"
  valueKey="num_deals"
/>
