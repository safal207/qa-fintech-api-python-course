# QA в финтехе: API-тестирование и автоматизация на Python

[![Course CI](https://github.com/safal207/qa-fintech-api-python-course/actions/workflows/ci.yml/badge.svg)](https://github.com/safal207/qa-fintech-api-python-course/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pytest](https://img.shields.io/badge/tests-pytest-green)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)

Научитесь тестировать платежи, балансы, комиссии, idempotency и негативные API-сценарии так, как это нужно в финтех-командах: не только по статусу `200 OK`, а по денежным, транзакционным и интеграционным рискам.

Курс ведёт к практическому результату: вы соберёте автотестовый проект на Python + Pytest + Allure + GitHub Actions, который можно показать в резюме, на собеседовании или использовать как основу для реальной QA-работы.

**Статус:** курс готовится к публикации на Stepik. Пока здесь лежит открытый sandbox-проект, программа и тестовая база.

## Быстрые действия

- Изучить программу: [docs/COURSE_OUTLINE.md](docs/COURSE_OUTLINE.md)
- Посмотреть позиционирование курса: [docs/POSITIONING.md](docs/POSITIONING.md)
- Запустить sandbox API локально: `uvicorn src.finpay_sandbox.api:app --reload`
- Прогнать автотесты: `python -m pytest`

## Для кого

- Manual QA, который хочет перейти в API-тестирование и автоматизацию.
- Junior/Middle QA, который хочет попасть в fintech, banking, brokerage или payments.
- QA-инженер, которому нужен портфолио-проект с Python, Pytest, API, Allure и CI.
- Тестировщик, который хочет увереннее говорить на собеседованиях про платежи, балансы, комиссии, retry и idempotency.

## Что вы соберёте

К концу курса у вас будет мини-проект, в котором есть:

- FastAPI sandbox с аккаунтами и переводами между счетами;
- тесты успешных и ошибочных денежных операций;
- проверки балансов после переводов;
- проверка комиссий и округлений;
- idempotency-тесты против двойного списания;
- негативные API-сценарии;
- контрактные проверки JSON Schema;
- Allure-результаты;
- GitHub Actions CI.

## Почему это не обычный курс по API

Обычный API-курс учит проверять статус-коды и поля JSON. Это полезно, но в финтехе ошибка часто стоит денег, доверия и разбирательств с поддержкой.

Здесь фокус на сценариях, где QA должен увидеть риск:

- деньги списались дважды;
- баланс после операции стал неверным;
- комиссия округлилась не по правилу;
- retry повторил платёж;
- idempotency key не защитил от повторного списания;
- перевод ушёл с несуществующего счёта;
- контракт ответа изменился и сломал клиента;
- CI не поймал регрессию до merge.

## Чему научитесь

- Разбирать денежную операцию как цепочку причин и последствий.
- Писать API-тесты на Python и Pytest.
- Проверять бизнес-инварианты: баланс, сумма, комиссия, статус операции.
- Тестировать негативные сценарии и ошибки домена.
- Валидировать JSON-контракты.
- Подключать Allure-отчёты и GitHub Actions.
- Описывать финтех-дефекты языком продукта, а не только кодом ответа.

## Программа

1. Финтех-мышление QA: деньги, балансы, комиссии, операционные риски.
2. База REST API: методы, статусы, JSON, Swagger/Postman, ручные проверки.
3. Python + Pytest: фикстуры, параметризация, helpers, структура тестов.
4. Финтех-сценарии: переводы, insufficient funds, комиссии, повторные запросы.
5. Контрактное тестирование: JSON Schema, обязательные поля, обратная совместимость.
6. CI и отчёты: GitHub Actions, Allure results, проверка качества pull request.

Полная версия: [docs/COURSE_OUTLINE.md](docs/COURSE_OUTLINE.md)

## Быстрый старт для проекта

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m pytest
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

## Структура

```text
.
├── docs/
│   ├── COURSE_OUTLINE.md
│   ├── ROADMAP.md
│   └── POSITIONING.md
├── src/finpay_sandbox/
│   ├── api.py
│   ├── domain.py
│   └── models.py
├── tests/
│   ├── api/
│   ├── contract/
│   └── domain/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

## Авторский фокус

Если ошибка может затронуть деньги пользователя, мы тестируем не “ответ API”, а всю причинно-денежную цепочку операции: запрос, бизнес-правило, баланс, комиссию, повторную попытку, контракт и регрессию в CI.
