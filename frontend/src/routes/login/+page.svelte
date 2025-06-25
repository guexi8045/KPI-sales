<script lang="ts">
  import { goto } from '$app/navigation';
  let username = '';
  let password = '';
  let error = '';

  async function handleLogin() {
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('token', data.token);
      goto('/');
    } else {
      error = 'Login fehlgeschlagen.';
    }
  }
</script>

<h1>Login</h1>
<form on:submit|preventDefault={handleLogin}>
  <label>Benutzername: <input bind:value={username} required /></label><br />
  <label>Passwort: <input type="password" bind:value={password} required /></label><br />
  <button type="submit">Anmelden</button>
  {#if error}<p style="color: red;">{error}</p>{/if}
</form>
