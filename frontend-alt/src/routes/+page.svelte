<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		const token = localStorage.getItem('token');
		if (!token) goto('/login');
	});
</script>

<style>
	.container {
		padding: 2rem;
		max-width: 900px;
		margin: auto;
	}

	h1 {
		font-size: 2rem;
		color: #222;
		margin-bottom: 1rem;
	}

	.info-box {
		background-color: #f2f2f2;
		border-left: 5px solid #007acc;
		padding: 1.2rem 1.5rem;
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

	ul.report-links {
		list-style-type: none;
		padding-left: 0;
		margin-top: 2rem;
	}

	ul.report-links li {
		margin-bottom: 0.4rem;
	}

	ul.report-links a {
		color: #007acc;
		text-decoration: none;
	}

	ul.report-links a:hover {
		text-decoration: underline;
	}
</style>

<div class="container">
	<h1>Welcome to the Güxi Sales KPIs</h1>

	<div class="info-box">
		<strong>Allgemeine Informationen zu den KPIs</strong>
		<ul>
			<li>
				@Sales: Bitte bezüglich der Erfassung genau an den Informationen aus der Schulung und dem Leitfaden unter
				<i>Dropbox/Administration/Prozesse…/Sales/PipedriveBI</i> orientieren und bei Unsicherheiten fragen kommen.
				Die Kennzahlen müssen spätestens bei Vertragsversand korrekt erfasst und kontrolliert werden.

			</li>
			<li>Kennzahlen für Kündigungen enthalten nicht die regulären KIGA Austritte

			</li>
			<li>
				Bei 2 Mutationen in einem Vertrag z.B. erst von 2 auf 3, dann von 3 auf 4 Tage wird direkt der Verkauf von 2 neuen Tagen an Bestandeskunden erfasst.
				Ebenso wenn ein Neukunde bei Vertragsabschluss bereits eine Mutation anmeldet (zb er bucht 3 Tage, sagt aber schon, dass er 3 Monate nach Start auf 2 Tage reduziert), 
				dann wird direkt ein Abschluss von 2 Tagen erfasst und nicht Abschluss + Mutation.
				
			</li>
			<li>
				Bei Kind mit mehreren Standorten: Abschluss und Kündigung wird dem Hauptstandort (Innengruppe, nicht Wald) zugeordnet.
				Ebenso wenn ein Kind auf 2 Standorten gebucht hat, es wird immer die Innengruppe getrackt.

			</li>
			<li>
				Problem: Wenn Eltern 2 Kinder anwählen wäre gut beide in einem Deal bearbeiten zu können, sodass als 1 Abschluss gezählt wird. Geht nicht bei z.B. 2×3 Tage, weil Anzahl Tage eines Abschlusses max. 5.
				→ Vorgehen: Deal nach Abschluss duplizieren, damit pro Kind ein Deal existiert (vorausgefüllt).
				→ Gibt leichte Verfälschung der Abschlusszahlen (selten) und betrifft nur die Anzahl Abschlüsse nicht die Anzahl Tage.

			</li>
			<li>Kündigung vor Start wird als Absage erfasst – nicht als Abschluss + Kündigung

			</li>
			<li>Mutation vor Start wird wie eine normale Mutation behandelt

			</li>
		</ul>
	</div>

	<p><strong>Wähle einen Report:</strong></p>

	<ul class="report-links">
		<li><a href="/absagegruende">Absagegründe</a></li>
		<li><a href="/abschluesse_alter">Abschlüsse Alter</a></li>
		<li><a href="/abschluesse_anzahl_tage">Abschlüsse Anzahl Tage</a></li>
		<li><a href="/abschluesse_finanzierung">Abschlüsse Finanzierung</a></li>
		<li><a href="/abschluesse_herkunft">Abschlüsse Herkunft</a></li>
		<li><a href="/abschluesse_standort">Abschlüsse Standort</a></li>
		<li><a href="/abschlussquote_krippenleitung">Abschlussquote Krippenleitung</a></li>
		<li><a href="/abschlussquote_standort">Abschlussquote Standort</a></li>
		<li><a href="/anfrage_kanal">Anfragekanal</a></li>
		<li><a href="/besichtigungen">Besichtigungen</a></li>
		<li><a href="/besichtigungen_standort">Besichtigungen Standort</a></li>
		<li><a href="/besichtigungsquote">Besichtigungsquote</a></li>
		<li><a href="/kuendigungen_grund">Kündigungsgründe</a></li>
		<li><a href="/kuendigungen_standort">Kündigungen Standort</a></li>
		<li><a href="/tage_abnahme">Tage Abnahme</a></li>
		<li><a href="/tage_abnahme_standort">Tage Abnahme Standort</a></li>
		<li><a href="/tage_entwicklung">Tage Entwicklung</a></li>
		<li><a href="/tage_entwicklung_standort">Tage Entwicklung Standort</a></li>
		<li><a href="/tage_zunahme">Tage Zunahme</a></li>
		<li><a href="/tage_zunahme_standort">Tage Zunahme Standort</a></li>
		<li><a href="/zeitbiseintritt">Zeit bis Eintritt</a></li>
		<li><a href="/datenbereinigung_p1deals">Datenbereinigung NK P1</a></li>
		<li><a href="/datenbereinigung_p1mutationen">Datenbereinigung Mutationen P1</a></li>
	</ul>
</div>
