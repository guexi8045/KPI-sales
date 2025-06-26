<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/absagegruende"
  title="Absagegründe pro Monat"
  valueKey="num_deals"
/>

