<script lang="ts">
  import { onMount } from 'svelte';
  import LineChart from '$lib/components/LineChart.svelte';
  import type { ChartData, ChartDataset } from 'chart.js';
  import html2canvas from 'html2canvas';
  import jsPDF from 'jspdf';

  interface AbschlussData {
    month: string;
    category_name: string;
    total_days: number;
  }

  let rawData: AbschlussData[] = [];
  let selectedCategories: string[] = [];
  let chartData: ChartData<'line'> | null = null;
  let chartContainer: HTMLDivElement;

  const fixedColors: string[] = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf'
  ];
  const categoryColors: Record<string, string> = {};
  const TOTAL_LABEL = 'Total';
  const TOTAL_COLOR = '#000000';

  let allCategories: string[] = [];

  const fetchData = async () => {
    const res = await fetch('http://127.0.0.1:5000/api/abschluesse_alter');
    rawData = await res.json();

    allCategories = [...new Set(rawData.map((d) => d.category_name))];
    selectedCategories = [...allCategories, TOTAL_LABEL];

    allCategories.forEach((cat, i) => {
      categoryColors[cat] = fixedColors[i % fixedColors.length];
    });
    categoryColors[TOTAL_LABEL] = TOTAL_COLOR;

    updateChartData();
  };

  function updateChartData() {
    const months = [...new Set(rawData.map((d) => d.month))].sort();
    const showTotal = selectedCategories.includes(TOTAL_LABEL);
    const shownCategories = selectedCategories.filter(c => c !== TOTAL_LABEL);

    const datasets: ChartDataset<'line'>[] = shownCategories.map((cat) => {
      const data = months.map((month) => {
        const record = rawData.find((d) => d.month === month && d.category_name === cat);
        return record ? record.total_days : 0;
      });

      return {
        label: cat,
        data,
        borderWidth: 2,
        tension: 0.3,
        borderColor: categoryColors[cat],
        backgroundColor: categoryColors[cat],
        pointBackgroundColor: categoryColors[cat],
        pointBorderColor: categoryColors[cat]
      };
    });

    if (showTotal) {
      const totalData = months.map(month => {
        return allCategories.reduce((sum, cat) => {
          const record = rawData.find((d) => d.month === month && d.category_name === cat);
          return sum + (record ? record.total_days : 0);
        }, 0);
      });

      datasets.push({
        label: TOTAL_LABEL,
        data: totalData,
        borderWidth: 3,
        borderDash: [6, 3],
        tension: 0.2,
        borderColor: TOTAL_COLOR,
        backgroundColor: TOTAL_COLOR,
        pointBackgroundColor: TOTAL_COLOR,
        pointBorderColor: TOTAL_COLOR
      });
    }

    chartData = {
      labels: months,
      datasets
    };
  }

  function exportPDF() {
    html2canvas(chartContainer).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('landscape');
      pdf.setFontSize(12);
      pdf.text('Abschlüsse nach Alter (Tage)', 14, 14);
      pdf.addImage(imgData, 'PNG', 10, 20, 270, 160);
      pdf.save('abschluesse_alter_report.pdf');
    });
  }

  function exportCSV() {
    const months = [...new Set(rawData.map((d) => d.month))].sort();
    const shownCats = selectedCategories.includes(TOTAL_LABEL)
      ? [...selectedCategories.filter(c => c !== TOTAL_LABEL), TOTAL_LABEL]
      : [...selectedCategories];

    const csvRows: string[] = [];
    csvRows.push(['Monat', ...shownCats].join(','));

    months.forEach(month => {
      const row = [month];
      shownCats.forEach(cat => {
        if (cat === TOTAL_LABEL) {
          const total = allCategories.reduce((sum, c) => {
            const r = rawData.find(d => d.month === month && d.category_name === c);
            return sum + (r ? r.total_days : 0);
          }, 0);
          row.push(total.toString());
        } else {
          const record = rawData.find((d) => d.month === month && d.category_name === cat);
          row.push(record ? record.total_days.toString() : '0');
        }
      });
      csvRows.push(row.join(','));
    });

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'abschluesse_alter.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  onMount(fetchData);
</script>

<h2>Abschlüsse nach Alter (in Tagen)</h2>

<div style="margin-bottom: 1rem; display: flex; flex-wrap: wrap;">
  {#each [...allCategories, TOTAL_LABEL] as cat}
    <label style="margin-right: 1rem; white-space: nowrap;">
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
  <button on:click={exportPDF}>📄 Export als PDF</button>
  <button on:click={exportCSV}>📊 Rohdaten als CSV</button>
</div>

{#if chartData}
  <div bind:this={chartContainer}>
    <LineChart
      {chartData}
      chartOptions={{
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
      }}
    />
  </div>
{:else}
  <p>Lade Diagramm...</p>
{/if}
