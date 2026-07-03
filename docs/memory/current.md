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
- Deploy non ancora eseguito: mancano canali, credenziali Telegram reali e, per publish reale, token bot.
- Preparazione della prima roadmap tecnica.
- Implementazione in corso del primo vertical slice operativo in `DRY_RUN`.

## Decisioni provvisorie

- Separare ingest, cleaning, validazione e publish.
- Non committare token bot, sessioni Telegram, password server o credenziali Portainer.
- Partire con SQLite se il volume e basso; passare a PostgreSQL se serve concorrenza o storico piu robusto.
- Usare Docker Compose sulla VM Docker esistente come primo target operativo.
- Tenere `DRY_RUN=true` nelle configurazioni iniziali fino al primo test controllato.
- Usare `VALIDATOR_MODE=local` come default iniziale.
- Impostare `STARTUP_BACKFILL_LIMIT=0` per evitare import storico.
- Impostare `RETENTION_DAYS=3` come default usa e getta.
- Salvare anche messaggi scartati in SQLite per poter raffinare parser/validator da esempi reali.

## Cosa puo fare Codex

- Implementare e testare scaffold, storage, parser, validatore locale, runner e Docker.
- Preparare deploy sulla VM Docker.
- Analizzare esempi reali anonimizzati e migliorare le regole.

## Cosa serve dall'utente

- `TELEGRAM_API_ID` e `TELEGRAM_API_HASH` da `my.telegram.org`.
- Account Telegram autorizzato a leggere i canali sorgente.
- Elenco `SOURCE_CHANNELS`.
- Quando si pubblichera davvero: bot token e canale destinazione privato.

## Domande aperte principali

- Elenco dei canali sorgente e tipo di accesso: pubblici, privati, admin, invite-only.
- Formato del post finale e politica link: link pulito, link originale, o nessun link.
- Esempi di messaggi reali da usare per raffinare parser e scarti.
