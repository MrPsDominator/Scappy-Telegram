# Current

## Stato attuale

- Progetto locale inizialmente vuoto secondo obiettivo utente; al controllo corrente e gia presente un repository Git locale senza commit.
- Repository remoto indicato dall'utente: `MrPsDominator/Scappy-Telegram`.
- Creato scaffold documentale e applicativo iniziale.
- Scelta tecnica proposta: Python, con Telethon per ingest Telegram e bot Telegram per pubblicazione.
- Target deploy previsto: Docker Compose sulla VM Docker/Portainer esistente.
- Verifica SSH non distruttiva su `root@docker.lan` completata: Docker remoto disponibile e Portainer attivo.
- Requisiti aggiornati dall'utente:
  - canali sorgente misti;
  - ingest solo nuovi messaggi;
  - retention breve di pochi giorni;
  - validatore esterno non disponibile ora;
  - uso personale, senza necessita di revisione manuale prima della pubblicazione.

## In corso

- Definizione dei requisiti funzionali.
- Preparazione dei confini del codice: ingest, cleaning, deduplica, validazione, publish.
- Deploy non ancora eseguito: mancano canali, token Telegram e URL validatore.
- Preparazione della prima roadmap tecnica.

## Decisioni provvisorie

- Separare ingest, cleaning, validazione e publish.
- Non committare token bot, sessioni Telegram, password server o credenziali Portainer.
- Partire con SQLite se il volume e basso; passare a PostgreSQL se serve concorrenza o storico piu robusto.
- Usare Docker Compose sulla VM Docker esistente come primo target operativo.
- Tenere `DRY_RUN=true` nelle configurazioni iniziali fino al primo test controllato.
- Usare `VALIDATOR_MODE=local` come default iniziale.
- Impostare `STARTUP_BACKFILL_LIMIT=0` per evitare import storico.
- Impostare `RETENTION_DAYS=3` come default usa e getta.

## Domande aperte principali

- Elenco dei canali sorgente e tipo di accesso: pubblici, privati, admin, invite-only.
- Formato del post finale e politica link: link pulito, link originale, o nessun link.
- Esempi di messaggi reali da usare per raffinare parser e scarti.
