<script lang="ts">
  import { onMount } from 'svelte';
  import LineChart from '$lib/components/LineChart.svelte';
  import type { ChartData, ChartDataset } from 'chart.js';
  import html2canvas from 'html2canvas';
  import jsPDF from 'jspdf';

  interface RawRecord {
    month: string;
    category_name: string;
    num_deals_abschluss: number;
    num_deals_absage: number;
  }

  interface ProcessedRecord {
    month: string;
    category_name: string;
    num_deals: number;
  }

  let rawData: RawRecord[] = [];
  let processedData: ProcessedRecord[] = [];

  let selectedCategories: string[] = [];
  let allCategories: string[] = [];

  let chartData: ChartData<'line'> | null = null;
  let chartContainer: HTMLDivElement;

  const TOTAL_LABEL = 'Total';
  const TOTAL_COLOR = '#000000';
  const endpoint = 'http://127.0.0.1:5000/api/abschlussquote_krippenleitung_roh';

  const fixedColors: string[] = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf', '#1a55FF', '#00C49F',
    '#f4a261', '#264653', '#e76f51', '#6a994e',
    '#9c27b0', '#3f51b5', '#009688', '#cddc39'
  ];

  const categoryColors: Record<string, string> = {};

  let selectedCategory: string = '';
  let startMonth: string = '2025-01';
  let endMonth: string = '2025-06';
  let customQuote: string = 'n/a';

  function calculateCustomQuote() {
    if (!selectedCategory || !startMonth || !endMonth) return;

    const from = new Date(`${startMonth}-01`);
    const to = new Date(`${endMonth}-01`);

    const filtered = rawData.filter(r => {
      const date = new Date(`${r.month}-01`);
      return r.category_name === selectedCategory && date >= from && date <= to;
    });

    const abs = filtered.reduce((sum, r) => sum + (r.num_deals_abschluss || 0), 0);
    const rej = filtered.reduce((sum, r) => sum + (r.num_deals_absage || 0), 0);
    const total = abs + rej;
    customQuote = total > 0 ? `${(abs / total * 100).toFixed(1)} %` : 'n/a';
  }

  function updateChartData() {
    const months = [...new Set(processedData.map(d => d.month))].sort();
    const showTotal = selectedCategories.includes(TOTAL_LABEL);
    const activeCats = selectedCategories.filter(c => c !== TOTAL_LABEL);

    const datasets: ChartDataset<'line'>[] = activeCats.map(cat => {
      const data = months.map(month => {
        const record = processedData.find(d => d.month === month && d.category_name === cat);
        return record ? Number(record.num_deals) : 0;
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
        const filtered = rawData.filter(r => r.month === month);
        const abs = filtered.reduce((sum, r) => sum + (r.num_deals_abschluss || 0), 0);
        const rej = filtered.reduce((sum, r) => sum + (r.num_deals_absage || 0), 0);
        const total = abs + rej;
        return total > 0 ? +(abs / total * 100).toFixed(1) : 0;
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

    chartData = { labels: months, datasets };
  }

  async function fetchData() {
    const token = localStorage.getItem("token");

    const res = await fetch(endpoint, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    rawData = await res.json();

    const grouped = new Map<string, { abs: number, rej: number }>();
    rawData.forEach(r => {
      const key = `${r.month}_${r.category_name}`;
      if (!grouped.has(key)) grouped.set(key, { abs: 0, rej: 0 });
      grouped.get(key)!.abs += r.num_deals_abschluss || 0;
      grouped.get(key)!.rej += r.num_deals_absage || 0;
    });

    processedData = Array.from(grouped.entries()).map(([key, val]) => {
      const [month, category_name] = key.split('_');
      const total = val.abs + val.rej;
      return {
        month,
        category_name,
        num_deals: total > 0 ? +(val.abs / total * 100).toFixed(1) : 0
      };
    });

    allCategories = [...new Set(processedData.map(d => d.category_name))];
    selectedCategories = [...allCategories, TOTAL_LABEL];

    allCategories.forEach((cat, i) => {
      categoryColors[cat] = fixedColors[i % fixedColors.length];
    });
    categoryColors[TOTAL_LABEL] = TOTAL_COLOR;

    updateChartData();
    calculateCustomQuote();
  }

  function exportPDF() {
    html2canvas(chartContainer).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('landscape');
      pdf.setFontSize(12);
      pdf.text("Abschlussquote pro Krippenleitung", 14, 14);
      pdf.addImage(imgData, 'PNG', 10, 20, 270, 160);
      pdf.save(`abschlussquote_krippenleitung_report.pdf`);
    });
  }

  function exportCSV() {
    const months = [...new Set(processedData.map(d => d.month))].sort();
    const shownCats = selectedCategories.includes(TOTAL_LABEL)
      ? [...selectedCategories.filter(c => c !== TOTAL_LABEL), TOTAL_LABEL]
      : [...selectedCategories];

    const csvRows: string[] = [];
    csvRows.push(['Monat', ...shownCats].join(','));

    months.forEach(month => {
      const row: string[] = [month];
      shownCats.forEach(cat => {
        if (cat === TOTAL_LABEL) {
          const relevant = rawData.filter(r => r.month === month);
          const abs = relevant.reduce((sum, r) => sum + r.num_deals_abschluss, 0);
          const rej = relevant.reduce((sum, r) => sum + r.num_deals_absage, 0);
          const total = abs + rej;
          row.push(total > 0 ? (abs / total * 100).toFixed(1) : '0');
        } else {
          const record = processedData.find(d => d.month === month && d.category_name === cat);
          row.push(record ? String(record.num_deals) : '0');
        }
      });
      csvRows.push(row.join(','));
    });

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `abschlussquote_krippenleitung_data.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function unselectAll() {
    selectedCategories = selectedCategories.includes(TOTAL_LABEL) ? [TOTAL_LABEL] : [];
    updateChartData();
  }

  onMount(fetchData);
</script>

<h2>Abschlussquote pro Krippenleitung</h2>

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
  <button on:click={unselectAll} style="margin-left: 1rem;">Unselect all</button>
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
        plugins: { legend: { position: 'bottom' } },
        scales: {
          y: {
            min: 0,
            max: 100,
            title: { display: true, text: 'Abschlussquote in %' }
          }
        }
      }}
    />
  </div>
{:else}
  <p>Lade Diagramm...</p>
{/if}

<hr style="margin: 2rem 0;" />

<div>
  <h4>Eigene Analyse</h4>
  <label>Kategorie:
    <select bind:value={selectedCategory} on:change={calculateCustomQuote}>
      {#each allCategories as cat}
        <option value={cat}>{cat}</option>
      {/each}
    </select>
  </label>
  <label style="margin-left: 1rem;">Zeitraum:
    <input type="month" bind:value={startMonth} on:change={calculateCustomQuote}>
    bis
    <input type="month" bind:value={endMonth} on:change={calculateCustomQuote}>
  </label>
  <p>Abschlussquote für <strong>{selectedCategory}</strong> im Zeitraum <strong>{startMonth}</strong> – <strong>{endMonth}</strong>: <strong>{customQuote}</strong></p>
</div>
