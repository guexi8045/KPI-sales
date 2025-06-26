<script lang="ts">
  import {
    Chart,
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Title,
    Tooltip,
    Legend,
    type ChartData,
    type ChartOptions
  } from 'chart.js';
  import { onMount } from 'svelte';

  export let chartData: ChartData<'line'>;
  export let chartOptions: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#333',
          font: {
            size: 12
          }
        }
      },
      title: {
        display: false
      },
      tooltip: {
        mode: 'index',
        intersect: false
      }
    },
    scales: {
      x: {
        ticks: { color: '#333' },
        grid: {
          color: 'rgba(0,0,0,0.05)'
        }
      },
      y: {
        ticks: { color: '#333' },
        grid: {
          color: 'rgba(0,0,0,0.05)'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  let canvas: HTMLCanvasElement;
  let chart: Chart<'line'>;

  Chart.register(
    LineController,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Title,
    Tooltip,
    Legend
  );

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'line',
      data: chartData,
      options: chartOptions
    });

    return () => chart.destroy();
  });

  $: if (chart && chartData) {
    chart.data = chartData;
    chart.update();
  }
</script>

<style>
  .chart-container {
    position: relative;
    width: 100%;
    max-width: 1000px;
    height: 500px;
    margin: 2rem auto;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>

<div class="chart-container">
  <canvas bind:this={canvas}></canvas>
</div>
