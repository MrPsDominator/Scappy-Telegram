# Changelog

## 2026-07-03

- Avviata definizione del progetto Scappy Telegram.
- Creato scaffold documentale iniziale.
- Aggiunti documenti di memoria: current, roadmap, changelog.
- Aggiunta architettura iniziale della pipeline.
- Aggiunto scaffold applicativo Python con confini per ingest, cleaning, deduplica, validazione, storage e publish.
- Aggiunti test iniziali per configurazione, pulizia URL e fingerprint candidati.
- Aggiunta `.dockerignore`.
- Aggiunta documentazione deploy VM in `docs/deploy.md`.
- Verificato accesso SSH non distruttivo a `root@docker.lan` e presenza Docker/Portainer.
- Registrate decisioni prodotto: canali misti, solo nuovi messaggi, retention breve, uso personale.
- Reso il validatore HTTP opzionale e aggiunto validatore locale iniziale.
- Aggiunte configurazioni `VALIDATOR_MODE`, `RETENTION_DAYS` e `STARTUP_BACKFILL_LIMIT`.

## 2026-07-04

- Aggiunti comandi CLI `run`, `login`, `init-db` e `check-config`.
- Aggiunto runner operativo per ascoltare nuovi messaggi Telegram in `DRY_RUN`.
- Esteso storage SQLite con tabella `raw_messages` per messaggi grezzi, scarti e duplicati.
- Aggiornato worker per restituire decisioni di pipeline strutturate.
- Aggiunto supporto per canali sorgente configurati come username o ID numerici.
