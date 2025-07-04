# GUEXI Reporting App\n\nProjekt zur Visualisierung und Bereitstellung von Reports über ein Webinterface.
Load Deals und Load Mutationen scrapt die Daten aus den beiden Salespipelines (ID = 1 / 37). init_pg_schema definiert das Schema der Datenbank.

Es handelt sich um eine PostgreSQL Datenbank die über das docker-compose File läuft.

Drop Tables wird genutzt, um die Datenbank zu leeren, bevor das Skript erneut ausgeführt wird, um allfällig in Pipedrive falsch angelegte Deals, die nun gelöscht wurden, dann auch nicht mehr in der Datenbank zu haben.

Berechnungen: Die Python Files im Ordner /reports stellen die Methoden zur Berechnung der einzelnen Reports zur Verfügung + 2 Scripts welche nach falsch ausgefüllten Deals zur Datenbereinigung suchen.

Backend mit Flask: /backend/routes Files enthalten je eine REST-API Route (als Flask Blueprint). Sie importierten die Funktion zur Berechnung aus /reports.
/backend/routes/__init__.py ist ein zentraler Verwaltungsort zur Registrierung aller Flask Routen. Importiert die Blueprints und bindet sie an die Flask App.
/backend/app.py Startpunkt der Flask-Anwendung

Frontend mit Svelte: /frontend/src/lib/components enthält die "Vorlagen" für die einzelnen Frontend-Report-Seiten.
/frontend/src/routes enthält die einzelnen Frontend-Seiten und nutzt die "Vorlage" ReportPage.svelte.
Lediglich die Abschlussquoten wurden unabhängig von ReportPage.svelte erstellt.

Github Actions für automatisches Aktualisieren der Daten über Nacht.