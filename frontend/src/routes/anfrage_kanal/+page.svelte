<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/anfrage_kanal"
  title="Anzahl Anfragen nach Kanal"
  valueKey="num_deals"
/>
