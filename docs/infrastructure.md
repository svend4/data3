# Инфраструктура и развёртывание

## Целевой ландшафт

- **Frontend**: SPA (React/Vue) с адаптивностью и доступностью.
- **Backend**: API (Python/FastAPI или Node.js).
- **БД**: PostgreSQL + шифрование на уровне диска.
- **Документы**: S3-совместимое хранилище (MinIO/Cloud).
- **Очереди**: RabbitMQ/Kafka для фоновых задач.
- **Auth**: Keycloak или другой OIDC провайдер.
- **Observability**: Grafana + Prometheus + Loki.

## Схема окружений

- **Dev**: локально с Docker Compose.
- **Stage**: тестовый кластер (Kubernetes).
- **Prod**: отдельный кластер с мульти-тенантностью.

## Пример Docker Compose (скелет)

```yaml
version: "3.9"
services:
  api:
    build: .
    environment:
      DATABASE_URL: postgres://budget:budget@db:5432/budget
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: budget
      POSTGRES_PASSWORD: budget
      POSTGRES_DB: budget
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

## Требования к безопасности

- Изоляция окружений, отдельные VPC.
- Резервные копии с шифрованием.
- Реагирование на инциденты и аудиторские логи.

## Требования к соответствию

- GDPR/BDSG: минимизация данных, права субъектов, журналирование.
- BITV 2.0: доступность интерфейсов.
