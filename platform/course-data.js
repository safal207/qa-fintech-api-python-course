window.courseModules = [
  {
    id: 'm1',
    title: '1. FinTech QA mindset',
    subtitle: 'Почему 200 OK не означает, что деньги в безопасности.',
    body: [
      'В финтехе QA проверяет не только HTTP-ответ. Он проверяет денежную цепочку: операция, баланс, комиссия, повтор запроса и след расследования.',
      'Главный навык этого модуля: видеть бизнес-риск за техническим ответом API.',
      'Если перевод прошёл, но баланс стал неверным, система не прошла проверку качества.'
    ],
    tasks: [
      'Объясни, почему 200 OK может скрывать дефект.',
      'Назови 3 риска при переводе денег.',
      'Открой README и найди список финтех-багов.'
    ],
    commands: 'git clone https://github.com/safal207/qa-fintech-api-python-course.git\ncd qa-fintech-api-python-course'
  },
  {
    id: 'm2',
    title: '2. Local setup',
    subtitle: 'Поднимаем окружение студента.',
    body: [
      'Перед автотестами студент должен уметь запустить проект локально.',
      'Мы используем Python 3.11+, virtualenv и requirements.txt.',
      'Цель шага: получить зелёный pytest локально.'
    ],
    tasks: [
      'Создай виртуальное окружение.',
      'Установи зависимости.',
      'Запусти pytest.'
    ],
    commands: 'python -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npytest'
  },
  {
    id: 'm3',
    title: '3. Sandbox API',
    subtitle: 'Изучаем учебный API для аккаунтов и переводов.',
    body: [
      'Sandbox API имитирует простую финтех-систему: аккаунты, балансы, перевод и сброс состояния.',
      'Это не production-сервис, а тренажёр для QA-мышления.',
      'Важно понимать, какой endpoint за что отвечает.'
    ],
    tasks: [
      'Запусти FastAPI приложение.',
      'Открой /health.',
      'Проверь /accounts/acc_alex.'
    ],
    commands: 'uvicorn src.finpay_sandbox.api:app --reload\ncurl http://127.0.0.1:8000/health\ncurl http://127.0.0.1:8000/accounts/acc_alex'
  },
  {
    id: 'm4',
    title: '4. Transfer tests',
    subtitle: 'Проверяем перевод, комиссию и балансы.',
    body: [
      'Главный сценарий курса: перевод денег между двумя аккаунтами.',
      'QA должен проверить баланс отправителя, баланс получателя и комиссию.',
      'Это уже бизнес-инвариант, а не просто status_code.'
    ],
    tasks: [
      'Открой tests/api/test_transfer.py.',
      'Найди проверку комиссии.',
      'Найди проверку баланса после перевода.'
    ],
    commands: 'pytest tests/api/test_transfer.py -q'
  },
  {
    id: 'm5',
    title: '5. Idempotency',
    subtitle: 'Защищаем пользователя от двойного списания.',
    body: [
      'Idempotency key нужен, чтобы повторный запрос не создал повторное списание.',
      'Это один из самых важных финтех-паттернов для API-тестирования.',
      'Хороший QA обязан проверять retry-сценарии.'
    ],
    tasks: [
      'Найди тест same idempotency key.',
      'Объясни, почему transfer_id должен совпадать.',
      'Проверь, что баланс после второго запроса не изменился.'
    ],
    commands: 'pytest tests/api/test_transfer.py::test_same_idempotency_key_does_not_charge_twice -q'
  },
  {
    id: 'm6',
    title: '6. Contract tests',
    subtitle: 'Проверяем стабильность API-ответов.',
    body: [
      'Контрактные тесты проверяют структуру ответа: обязательные поля, типы и совместимость.',
      'Если API внезапно меняет поле, клиент может сломаться.',
      'В курсе используется JSON Schema.'
    ],
    tasks: [
      'Открой tests/contract.',
      'Посмотри required поля.',
      'Запусти contract tests отдельно.'
    ],
    commands: 'pytest tests/contract -q'
  },
  {
    id: 'm7',
    title: '7. CI and Allure',
    subtitle: 'Запускаем тесты автоматически.',
    body: [
      'CI показывает, что проект можно проверять не только на машине автора.',
      'GitHub Actions запускает pytest и собирает Allure results.',
      'Это важная часть портфолио QA Automation.'
    ],
    tasks: [
      'Открой .github/workflows/ci.yml.',
      'Проверь шаг Run tests.',
      'Проверь artifact allure-results.'
    ],
    commands: 'pytest --alluredir=allure-results\n# then open GitHub Actions artifacts'
  },
  {
    id: 'm8',
    title: '8. Final project',
    subtitle: 'Оформляем работу для портфолио.',
    body: [
      'Финальный результат студента — GitHub-репозиторий с тестами, CI и понятным README.',
      'Важно описывать не только код, но и финтех-риски, которые покрывают тесты.',
      'Такой проект можно показать на собеседовании.'
    ],
    tasks: [
      'Сделай fork репозитория.',
      'Добавь один новый негативный тест.',
      'Оформи README своего проекта.'
    ],
    commands: 'git checkout -b student-final-project\npytest\ngit status'
  }
];
