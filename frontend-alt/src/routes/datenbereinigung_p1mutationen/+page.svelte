<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let ids: number[] = [];
  let loading = true;

  async function fetchData() {
    const token = localStorage.getItem('token');
    const res = await fetch('http://127.0.0.1:5000/api/datenbereinigung_p1mutationen', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (res.status === 401) {
      alert('Nicht eingeloggt. Bitte erneut anmelden.');
      localStorage.removeItem('token');
      goto('/login');
      return;
    }

    ids = await res.json();
    loading = false;
  }

  onMount(fetchData);
</script>

<div style="padding: 2rem; max-width: 800px; margin: auto;">
  <h2 style="font-size: 1.8rem; margin-bottom: 1rem;">Datenbereinigung: Fehlende oder inkonsistente Mutationen</h2>

  <div style="background-color: #f3f4f6; padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
    <strong>Hinweis:</strong> Es werden Mutationen angezeigt, die mindestens einen der folgenden Fehler enthalten:
    <ul style="margin-top: 0.5rem; padding-left: 1.5rem; list-style-type: disc;">
      <li>Die Mutation hat ein Abschlussdatum, aber der Standort ist leer</li>
      <li>Die Mutation hat ein Abschlussdatum, aber sowohl Mutationstage als auch Kündigungstage sind leer</li>
      <li>Kündigungstage erfasst, aber der Kündigungsgrund ist leer</li>
    </ul>
  </div>

  {#if loading}
    <p>Lade Daten...</p>
  {:else if ids.length === 0}
    <p>Keine fehlerhaften Einträge gefunden.</p>
  {:else}
    <p><strong>Folgende Deal-IDs</strong> weisen potenziell fehlerhafte oder unvollständige Daten auf:</p>
    <ul style="padding-left: 1.5rem;">
      {#each ids as id}
        <li>
          <a href={`https://guexi.pipedrive.com/deal/${id}`} target="_blank" rel="noopener noreferrer">
            Deal {id}
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</div>
