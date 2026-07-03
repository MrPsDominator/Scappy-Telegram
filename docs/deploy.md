# Deploy VM Docker

Target attuale: VM raggiungibile via SSH con:

```powershell
ssh root@docker.lan
```

Verifica gia eseguita:

- host: `docker`
- Docker disponibile: `Docker version 29.6.1`
- Portainer presente come container `portainer`

## Strategia consigliata

Non deployare finche mancano canali e token Telegram. Il validatore puo partire in modalita locale con `VALIDATOR_MODE=local`. Quando i requisiti sono chiari:

1. creare una directory dedicata sulla VM, per esempio `/opt/scappy-telegram`;
2. copiare o clonare il progetto;
3. creare `/opt/scappy-telegram/.env` direttamente sulla VM;
4. avviare con `docker compose up -d --build`;
5. verificare log con `docker compose logs -f scappy-telegram`.

## Esempio manuale

```powershell
ssh root@docker.lan "mkdir -p /opt/scappy-telegram"
scp Dockerfile compose.yaml pyproject.toml README.md .env.example root@docker.lan:/opt/scappy-telegram/
scp -r src docs tests root@docker.lan:/opt/scappy-telegram/
ssh root@docker.lan "cd /opt/scappy-telegram && cp .env.example .env"
```

Poi modificare `.env` sulla VM e avviare:

```bash
cd /opt/scappy-telegram
docker compose up -d --build
docker compose logs -f scappy-telegram
```

## Note sicurezza

- Non salvare password Portainer, token bot, sessioni Telethon o `.env` nel repository.
- Il volume `scappy_telegram_data` contiene database e sessione Telegram: va trattato come dato sensibile.
- Prima di attivare `DRY_RUN=false`, fare un test su un canale destinazione privato.
