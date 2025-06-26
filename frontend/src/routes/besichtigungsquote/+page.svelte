<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/besichtigungsquote"
  title="Besichtigungsquote: Wie gut haben wir unsere Besichtigungen verkauft? | a/(a+b)  a = Anzahl in diesem Monat durchgeführte Besichtigungen | b = Anzahl Anfragen die in diesem Monat zu einer Absage führten"
  valueKey="num_deals"
/>
