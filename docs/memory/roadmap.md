# Roadmap

## Fase 0 - Setup progetto

- [x] Inizializzare Git locale.
- [ ] Collegare il repository remoto GitHub.
- [x] Definire struttura Python, configurazione e Docker Compose.
- [x] Creare file `.env.example` con placeholder sicuri.
- [x] Creare documenti memoria: current, roadmap, changelog.
- [x] Documentare procedura iniziale di deploy VM.
- [ ] Documentare procedura completa di login Telethon.

## Fase 1 - Proof of concept Telegram

- [ ] Autenticare una sessione Telegram autorizzata.
- [ ] Leggere messaggi da un canale sorgente di test.
- [ ] Avviare listener solo nuovi messaggi, senza backfill storico.
- [ ] Salvare messaggi grezzi e metadati minimi.
- [ ] Pubblicare un messaggio di test nel canale finale tramite bot.
- [x] Verificare accesso SSH e Docker sulla VM senza toccare le altre stack.
- [ ] Verificare deploy container sulla VM Docker senza toccare le altre stack.

## Fase 2 - Parsing e pulizia

- [ ] Estrarre titolo, prezzo, valuta, link e sorgente.
- [x] Aggiungere prima estrazione del prezzo corrente.
- [x] Aggiungere prima estrazione del prezzo precedente.
- [ ] Normalizzare URL e rimuovere parametri tracking comuni.
- [ ] Definire regole per identificare e rimuovere link affiliati.
- [ ] Gestire messaggi con immagini, bottoni inline e link multipli.
- [ ] Aggiungere test con esempi reali anonimizzati.

## Fase 3 - Deduplica e validazione

- [ ] Implementare hash prodotto/link/prezzo.
- [ ] Evitare ripubblicazioni dello stesso annuncio.
- [x] Aggiungere validatore locale iniziale a regole.
- [ ] Collegare eventuale validatore prezzo/prodotto evoluto.
- [ ] Registrare motivi di approvazione/scarto.
- [ ] Definire policy per retry e fallback quando il validatore non risponde.
- [ ] Implementare cleanup retention pochi giorni.

## Fase 4 - Deploy

- [x] Preparare container Docker base.
- [x] Configurare Docker Compose base.
- [ ] Configurare Compose per VM/Portainer.
- [ ] Montare volume persistente per database e sessione Telegram.
- [ ] Aggiungere logging e restart policy.
- [ ] Definire backup database/sessione.

## Fase 5 - Operativita

- [ ] Dashboard o comandi admin minimi.
- [ ] Alert su errori di ingest, validazione o publish.
- [ ] Backup database/sessione.
- [ ] Regole avanzate per canale sorgente e categoria prodotto.
- [ ] Metriche minime: messaggi letti, candidati, approvati, scartati, pubblicati.
