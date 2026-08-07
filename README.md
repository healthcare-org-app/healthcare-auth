# auth-service

auth-service — domain: auth

- **Port:** 8002
- **Language:** Python 3.11 + Flask
- **Database:** `auth` (Postgres, table `auth`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/auth/`          |
| POST      | `/api/auth/`          |
| GET       | `/api/auth/<id>`      |
| PUT/PATCH | `/api/auth/<id>`      |
| DELETE    | `/api/auth/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** auth.session.started
**Subscribes:** identity.user.deactivated

## HTTP peer dependencies

- `identity-service`
- `authorization-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
