<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let ids: number[] = [];
  let loading = true;

  async function fetchData() {
    const token = localStorage.getItem('token');
    const res = await fetch('http://127.0.0.1:5000/api/datenbereinigung_p1deals', {
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

<style>
  .container {
    padding: 2rem;
    max-width: 800px;
    margin: auto;
  }

  h2 {
    margin-bottom: 0.5rem;
    font-size: 1.8rem;
    color: #333;
  }

  .info-box {
    background-color: #f2f2f2;
    border-left: 5px solid #007acc;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    font-size: 0.95rem;
    color: #444;
  }

  .info-box ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-top: 0.5rem;
  }

  .info-box ul ul {
    list-style-type: disc;
    padding-left: 1.5rem;
  }

  .section {
    margin-bottom: 2rem;
  }

  ul {
    padding-left: 1.5rem;
  }

  li {
    margin-bottom: 0.4rem;
  }

  a {
    color: #007acc;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }
</style>

<div class="container">
  <h2>Datenbereinigung: Fehlende oder inkonsistente Deals</h2>

  <div class="info-box">
    <strong>Hinweis:</strong> Es werden Deals angezeigt, welche mindestens einen der folgenden Fehler enthalten:
    <ul>
      <li>Deals die ein Absagedatum haben aber keinen Absagegrund</li>
      <li>Deals die einen Absagegrund haben aber kein Absagedatum</li>
      <li>Die Deals haben ein Abschlussdatum, aber:
        <ul>
          <li>Standort ist leer</li>
          <li>Anzahl Tage ist leer</li>
          <li>Krippenleitung ist "Keine Besichtigung", aber es existiert trotzdem ein Besichtigungsdatum</li>
          <li>Alter beim Eintritt ist leer</li>
          <li>ein Absagedatum ist gesetzt (obwohl abgeschlossen)</li>
          <li>es fehlt ein Besichtigungsdatum, obwohl die Krippenleitung nicht "Keine Besichtigung" ist</li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="section">
    {#if loading}
      <p>Lade Daten...</p>
    {:else if ids.length === 0}
      <p>Keine fehlerhaften Einträge gefunden.</p>
    {:else}
      <p><strong>Folgende Deal-IDs</strong> weisen potenziell fehlerhafte oder unvollständige Daten auf:</p>
      <ul>
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
</div>
