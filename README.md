# QA в финтехе: API-тестирование и автоматизация на Python

Практический репозиторий для курса на Stepik.

**Главная идея курса:** научить QA-инженера тестировать финтеховые API не на уровне `200 OK`, а на уровне денежных, транзакционных и интеграционных рисков.

## Для кого курс

- Manual QA, который хочет перейти в API и автоматизацию.
- Junior/Middle QA, который хочет попасть в fintech/banking/brokerage/payments.
- QA-инженер, которому нужен проект в портфолио: Python + Pytest + API + Allure + CI.

## Что студент соберёт

К концу курса студент соберёт мини-проект:

- тесты переводов между счетами;
- проверку балансов после операций;
- проверку комиссий и округлений;
- idempotency-тесты против двойного списания;
- негативные API-сценарии;
- контрактные проверки JSON Schema;
- отчёт Allure;
- GitHub Actions CI.

## Почему это не обычный курс по API

Обычный API-курс учит проверять статус-коды и поля JSON.

Этот курс учит видеть финтеховые баги:

- деньги списались дважды;
- баланс в API и UI не совпадает;
- комиссия округлилась неверно;
- retry привёл к повторной операции;
- лимит применился после списания;
- audit log не содержит причины операции;
- webhook пришёл дважды;
- транзакция зависла в `processing`.

## Стек

- Python 3.11+
- Pytest
- FastAPI sandbox
- HTTPX
- Pydantic
- JSON Schema
- Allure
- GitHub Actions
- Docker / docker-compose

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest
```

Запуск sandbox API:

```bash
uvicorn src.finpay_sandbox.api:app --reload
```

Запуск тестов с Allure:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## Структура

```text
.
├── docs/
│   ├── COURSE_OUTLINE.md
│   ├── ROADMAP.md
│   └── POSITIONING.md
├── modules/
│   └── ...
├── src/finpay_sandbox/
│   ├── api.py
│   ├── domain.py
│   └── models.py
├── tests/
│   ├── api/
│   ├── contract/
│   └── domain/
├── .github/workflows/ci.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

## Авторский фокус

Курс построен вокруг мышления QA в финтехе:

> Если ошибка может затронуть деньги пользователя, мы тестируем не “ответ API”, а всю причинно-денежную цепочку операции.

