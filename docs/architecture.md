# Architettura iniziale

## Pipeline

```text
Canali Telegram sorgente
        |
        v
Ingestor Telegram
        |
        v
Parser e cleaner
        |
        v
Deduplica e storage
        |
        v
Validatore prezzo/prodotto
        |
        v
Publisher Telegram Bot
        |
        v
Canale Telegram finale
```

## Componenti

### Ingestor Telegram

Legge messaggi dai canali sorgente. In Python la scelta piu pratica e Telethon, usando una sessione Telegram autorizzata per i canali che non sono leggibili da un bot.

Responsabilita:

- collegarsi con `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` e sessione persistente;
- ascoltare nuovi messaggi;
- non importare lo storico per default (`STARTUP_BACKFILL_LIMIT=0`);
- salvare metadati minimi: canale, id messaggio, data, testo, link, media presenti.

### Parser e cleaner

Normalizza il contenuto del messaggio:

- titolo/prodotto;
- prezzo;
- valuta;
- link;
- eventuale negozio o marketplace;
- rimozione di tracking, referrer e link affiliati dove riconoscibili;
- rimozione di testo promozionale o boilerplate.

Il cleaner deve essere conservativo: meglio scartare un candidato ambiguo o mandarlo al validatore che rompere link prodotto validi.

### Deduplica e storage

Mantiene memoria delle offerte gia viste. All'inizio basta SQLite con volume Docker persistente; se il servizio cresce o deve girare con piu worker, si passa a PostgreSQL.

Tabelle iniziali:

- `raw_messages`: messaggi letti, inclusi scarti e duplicati, con retention breve;
- `offers`: candidati offerta, validazione e risultato publish.

Chiavi possibili:

- canale sorgente + id messaggio;
- fingerprint normalizzato di titolo + prezzo + link pulito;
- URL canonico prodotto quando disponibile.

### Validatore

Modulo separato che riceve un candidato prodotto e decide se pubblicarlo.

Versione iniziale:

- `VALIDATOR_MODE=local`;
- approva candidati con prezzo riconosciuto e titolo presente;
- scarta messaggi senza prezzo, comunicazioni generiche e contenuti non-offerta;
- conserva eventuale prezzo precedente se indicato nel testo.

Versioni future:

- `VALIDATOR_MODE=http` verso API esterna;
- LLM locale per classificazione e normalizzazione;
- integrazione con AIOS personale quando avra ricerca internet/storico prezzi.

### Publisher

Pubblica nel canale Telegram finale usando un bot Telegram amministratore del canale.

Deve ricevere solo offerte approvate. In caso di errore Telegram, il tentativo va registrato e ritentato senza duplicare.

## Stack consigliato

- Python 3.12+
- Telethon per Telegram client/user session
- python-telegram-bot oppure Bot API HTTP diretta per pubblicazione
- Pydantic per configurazione e modelli dati
- SQLite nella prima fase, PostgreSQL in produzione
- Docker Compose per deploy

## Moduli nello scaffold

- `config.py`: impostazioni da `.env`.
- `models.py`: modelli dati interni.
- `cleaning.py`: estrazione link, pulizia URL, prima estrazione candidato.
- `dedupe.py`: fingerprint stabile per non ripubblicare la stessa offerta.
- `validator.py`: validatore locale a regole o client HTTP esterno.
- `publisher.py`: pubblicazione via Bot API.
- `storage.py`: persistenza SQLite.
- `telegram_ingest.py`: confine Telethon.
- `worker.py`: orchestrazione pipeline.
- `runtime.py`: comandi operativi e loop del servizio.

## Comandi runtime

```text
scappy-telegram init-db       crea/aggiorna schema SQLite
scappy-telegram check-config  valida la configurazione per run
scappy-telegram login         crea sessione Telethon persistente
scappy-telegram run           ascolta nuovi messaggi e processa pipeline
```

Il comando `run` ascolta i nuovi messaggi. Il backfill e disabilitato per default con `STARTUP_BACKFILL_LIMIT=0`.

## Deploy previsto

La VM Docker esistente esporra il servizio come container Compose:

```text
compose.yaml
  scappy-telegram
    env_file: .env
    volume: scappy_telegram_data:/app/data
```

Nel volume persistono database SQLite e sessione Telethon. Le credenziali restano fuori dal repository.

## Vincoli da chiarire

- Quali canali sorgente devono essere letti e con quale account autorizzato.
- Regole esatte per rimuovere affiliate/tracking senza rompere link utili.
- Formato finale del post nel canale Telegram.
- Esempi reali di messaggi non-offerta da scartare.
