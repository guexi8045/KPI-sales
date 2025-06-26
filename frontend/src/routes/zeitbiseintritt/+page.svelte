<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="
  /api/zeitbiseintritt"
  title="Ø Tage zwischen Abschluss und Eintritt"
  valueKey="num_deals"
/>
