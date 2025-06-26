<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/zeitbiseintritt"
  title="Ø Tage zwischen Abschluss und Eintritt"
  valueKey="num_deals"
/>
