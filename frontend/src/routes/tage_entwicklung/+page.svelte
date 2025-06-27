<script lang="ts">
  import ReportPage from '$lib/components/ReportPage.svelte';
</script>

<ReportPage
  endpoint="/api/tage_entwicklung"
  title="Tage Entwicklung (Zunahme-Abnahme). Mutationen, Neukunden und Kündigungen berücksichtigt. Exkl. Grund = KIGA"
  valueKey="num_deals"
/>