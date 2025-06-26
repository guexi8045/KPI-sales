<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let token: string | null = null;

	onMount(() => {
		token = localStorage.getItem('token');
		const protectedPaths = [
			'/absagegruende', '/abschluesse_anzahl_tage', '/abschlussquote_krippenleitung',
			'/abschlussquote_standort', '/tage_abnahme', '/tage_entwicklung_standort',
			// … ergänze hier alle geschützten Report-Pfade
		];

		if (protectedPaths.includes(window.location.pathname) && !token) {
			goto('/login');
		}
	});
</script>

<slot />
