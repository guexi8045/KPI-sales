<script lang="ts">
  import { onMount } from 'svelte';
  import LineChart from '$lib/components/LineChart.svelte';
  import type { ChartData, ChartDataset } from 'chart.js';
  import * as FileSaver from 'file-saver';

  export let endpoint: string;
  export let title: string;
  export let valueKey: string = 'num_deals';

  interface ReportRecord {
    month: string;
    category_name: string;
    [key: string]: string | number;
  }

  let rawData: ReportRecord[] = [];
  let selectedCategories: string[] = [];
  let chartData: ChartData<'line'> | null = null;

  const fetchData = async () => {
    const res = await fetch(endpoint);
    rawData = await res.json();

    const allCategories = [...new Set(rawData.map(d => d.category_name))];
    selectedCategories = [...allCategories];
    updateChartData();
  };

  function updateChartData() {
    const months = [...new Set(rawData.map((d) => d.month))].sort();

    const datasets: ChartDataset<'line'>[] = selectedCategories.map((cat) => {
      const data = months.map((month) => {
        const record = rawData.find((d) => d.month === month && d.category_name === cat);
        return record ? Number(record[valueKey]) : 0;
      });

      return {
        label: cat,
        data,
        borderWidth: 2,
        tension: 0.3
      };
    });

    chartData = {
      labels: months,
      datasets
    };
  }

  function exportCSV() {
    const months = [...new Set(rawData.map(d => d.month))].sort();
    const header = ['Monat', ...selectedCategories];
    const rows = months.map(month => {
      const row: string[] = [month];
      for (const cat of selectedCategories) {
        const record = rawData.find(d => d.month === month && d.category_name === cat);
        row.push(record ? String(record[valueKey]) : '');
      }
      return row;
    });

    const csvContent = [header, ...rows].map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' ]);
    FileSaver.saveAs(blob, `${title.replace(/\s+/g, '_')}.csv`);
  }

  onMount(fetchData);
</script>

<h2>{title}</h2>

<div style="margin-bottom: 1rem;">
  {#each [...new Set(rawData.map(d => d.category_name))] as cat}
    <label style="margin-right: 1rem;">
      <input
        type="checkbox"
        bind:group={selectedCategories}
        value={cat}
        on:change={updateChartData}
        checked
      />
      {cat}
    </label>
  {/each}
</div>

<div style="margin-bottom: 1rem;">
  <button on:click={exportCSV}>📊 CSV exportieren</button>
</div>

{#if chartData}
  <LineChart
    {chartData}
    chartOptions={{
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }}
  />
{:else}
  <p>Lade Diagramm...</p>
{/if}
