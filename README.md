# Scappy Telegram

Tool per raccogliere annunci/offerte da canali Telegram autorizzati, ripulire testo e link inutili, deduplicare i prodotti e pubblicare in un unico canale Telegram solo offerte normalizzate e validate.

## Si puo fare?

Si, con due vincoli importanti:

- per leggere canali Telegram serve un account o bot che abbia accesso reale a quei canali;
- un bot Telegram da solo non puo leggere canali arbitrari: per molti casi serve una sessione utente via API Telegram/MTProto.

La strada pratica e usare un client Telegram per l'ingest e un bot Telegram amministratore per pubblicare nel canale finale.

## Obiettivo

Il sistema deve:

- leggere messaggi da canali Telegram sorgente accessibili;
- estrarre prodotto, prezzo, link originale e metadati utili;
- rimuovere rumore, tracking e link affiliati quando possibile;
- filtrare i candidati con un validatore locale iniziale, estendibile poi a API o LLM;
- pubblicare solo offerte approvate in un canale Telegram finale tramite bot;
- tenere traccia di duplicati, errori e decisioni di validazione.

## Stack proposto

Linguaggio principale: Python.

Motivi:

- librerie Telegram mature come Telethon;
- parsing testuale, normalizzazione URL e job asincroni semplici da gestire;
- facile containerizzazione Docker;
- integrazione naturale con API esterne per validazione prezzi;
- buona velocita di sviluppo per un progetto di automazione.

## Decisioni iniziali

- Canali sorgente misti: pubblici e privati.
- Ingest solo di nuovi messaggi, senza import storico.
- Retention breve: pochi giorni, default 3.
- Validazione iniziale locale a regole: prezzo rilevato, titolo presente, messaggi non-offerta scartati.
- Futuro validatore evoluto: API HTTP, AIOS personale o LLM locale quando sara utile.
- Uso personale, con pubblicazione automatica su canale privato quando `DRY_RUN=false`.

## Struttura prevista

```text
docs/
  architecture.md
  deploy.md
  memory/
    current.md
    roadmap.md
    changelog.md
src/
  scappy_telegram/
    __init__.py
    cleaning.py
    config.py
    dedupe.py
    models.py
    publisher.py
    storage.py
    telegram_ingest.py
    validator.py
    worker.py
tests/
```

## Nota Telegram

Un bot Telegram da solo non puo leggere liberamente tutti i canali esistenti. Per leggere canali sorgente servono canali dove il bot e membro/admin oppure una sessione Telegram utente autorizzata tramite API Telegram. La pubblicazione nel canale finale, invece, puo essere fatta con un bot amministratore del canale.

## Deployment

Target previsto: Docker Compose sulla VM Docker/Portainer esistente. Le credenziali e le sessioni Telegram non devono essere committate nel repository. Note operative in `docs/deploy.md`.

## Avvio locale

```powershell
python -m pip install -e .[dev]
Copy-Item .env.example .env
pytest
```

Poi compilare `.env` con credenziali Telegram, canali sorgente, bot di destinazione e URL del validatore.

## Domande aperte residue

- Il canale finale deve mostrare link originale pulito, link al negozio, o nessun link?
- Servono canali/categorie separate o basta un unico stream?
- Quali esempi reali di messaggi vanno scartati per primi?
