<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="http://127.0.0.1:5000/api/tage_entwicklung"
  title="Tage Entwicklung (Zunahme-Abnahme). Mutationen, Neukunden und Kündigungen berücksichtigt. Exkl. Grund = KIGA"
  valueKey="num_deals"
/>