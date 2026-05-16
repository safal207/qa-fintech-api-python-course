export type Lesson = {
  slug: string;
  title: string;
  tag: string;
  body: string[];
  tasks: string[];
  command: string;
};

export const lessons: Lesson[] = [
  {
    slug: '01-fintech-qa',
    title: 'FinTech QA mindset',
    tag: 'Risk thinking',
    body: [
      'В финтехе QA проверяет не только HTTP-ответ. Он проверяет денежную цепочку: операция, баланс, комиссия и повтор запроса.',
      'Главная идея: 200 OK не означает, что деньги пользователя в безопасности.',
    ],
    tasks: ['Объясни риск double charge.', 'Найди в README список финтех-багов.', 'Сформулируй один баг-репорт про неверный баланс.'],
    command: 'git clone https://github.com/safal207/qa-fintech-api-python-course.git\ncd qa-fintech-api-python-course',
  },
  {
    slug: '02-local-setup',
    title: 'Local setup',
    tag: 'Environment',
    body: ['Настраиваем Python-окружение и запускаем тесты локально.', 'Цель шага: получить зелёный pytest на своей машине.'],
    tasks: ['Создай virtualenv.', 'Установи requirements.', 'Запусти pytest.'],
    command: 'python -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npytest',
  },
  {
    slug: '03-sandbox-api',
    title: 'Sandbox API',
    tag: 'FastAPI',
    body: ['Изучаем учебный API: health, accounts, reset и transfer.', 'Этот API нужен как тренажёр для финтех-мышления.'],
    tasks: ['Запусти API.', 'Проверь /health.', 'Проверь /accounts/acc_alex.'],
    command: 'uvicorn src.finpay_sandbox.api:app --reload\ncurl http://127.0.0.1:8000/health',
  },
  {
    slug: '04-transfer-tests',
    title: 'Transfer tests',
    tag: 'Pytest',
    body: ['Проверяем перевод денег между аккаунтами.', 'QA должен проверить баланс отправителя, баланс получателя и комиссию.'],
    tasks: ['Открой test_transfer.py.', 'Найди проверку комиссии.', 'Найди проверку баланса после операции.'],
    command: 'pytest tests/api/test_transfer.py -q',
  },
  {
    slug: '05-idempotency',
    title: 'Idempotency',
    tag: 'Money safety',
    body: ['Idempotency key защищает пользователя от двойного списания при повторном запросе.', 'Это один из ключевых финтех-паттернов для API-тестирования.'],
    tasks: ['Найди тест idempotency.', 'Проверь, что transfer_id совпадает.', 'Проверь, что баланс не меняется второй раз.'],
    command: 'pytest tests/api/test_transfer.py::test_same_idempotency_key_does_not_charge_twice -q',
  },
  {
    slug: '06-contract-tests',
    title: 'Contract tests',
    tag: 'JSON Schema',
    body: ['Контрактные тесты проверяют структуру API-ответа.', 'Они защищают клиентов от внезапных изменений полей и типов.'],
    tasks: ['Открой tests/contract.', 'Посмотри required поля.', 'Запусти contract tests.'],
    command: 'pytest tests/contract -q',
  },
  {
    slug: '07-ci-allure',
    title: 'CI and Allure',
    tag: 'Automation',
    body: ['CI показывает, что проект проверяется не только на машине автора.', 'GitHub Actions запускает pytest и собирает Allure results.'],
    tasks: ['Открой workflow.', 'Проверь шаг Run tests.', 'Найди artifact allure-results.'],
    command: 'pytest --alluredir=allure-results',
  },
  {
    slug: '08-final-project',
    title: 'Final project',
    tag: 'Portfolio',
    body: ['Финальный результат — GitHub-репозиторий студента с тестами, CI и понятным README.', 'Важно описать финтех-риски, которые покрывают тесты.'],
    tasks: ['Сделай fork.', 'Добавь новый негативный тест.', 'Оформи README своего проекта.'],
    command: 'git checkout -b student-final-project\npytest\ngit status',
  },
];
