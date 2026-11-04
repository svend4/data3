# API контракт (черновик)

## Аутентификация

`POST /auth/token` — получение JWT (OIDC).

## Бюджеты

- `GET /budgets?user_id=...` — список бюджетов.
- `POST /budgets` — создать бюджетный план.
- `GET /budgets/{id}` — получить детали.

## Транзакции

- `POST /transactions` — создать транзакцию.
- `GET /transactions?budget_id=...` — список по бюджету.
- `POST /transactions/{id}/documents` — загрузка документа.

## Согласования

- `POST /approvals` — запрос согласования.
- `PATCH /approvals/{id}` — решение по запросу.

## Кейсы сопровождения

- `GET /cases` — список кейсов.
- `POST /cases` — создать кейс.
