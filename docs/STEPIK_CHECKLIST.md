# Stepik Course Checklist

## 1. Course page
- Add a clear title: QA in FinTech: API Testing and Python Automation.
- Explain that the course is about money-related API risks, not only status codes.
- Add the GitHub repository link.
- Add the final project result: fintech API tests with CI.

## 2. Free demo lessons
- Lesson 1: why 200 OK is not enough in fintech.
- Lesson 2: how to check balance after transfer.
- Lesson 3: how idempotency prevents double charge.

## 3. Student setup
- Install Python 3.11 or newer.
- Clone this repository.
- Create virtual environment.
- Install requirements.
- Run pytest.

## 4. Practice flow
- Start with manual API checks.
- Move to pytest automation.
- Add domain checks for money logic.
- Add contract tests.
- Run tests in GitHub Actions.

## 5. Final project
Student should submit:
- GitHub repository link.
- Test suite for accounts and transfers.
- Idempotency test.
- Contract tests.
- CI workflow screenshot or link.
- Short README explaining fintech risks.

## 6. Quality bar
The project is ready when:
- tests pass locally;
- CI is green;
- README is clear;
- test names explain business risk;
- code can be run by another student from scratch.
