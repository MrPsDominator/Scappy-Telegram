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
