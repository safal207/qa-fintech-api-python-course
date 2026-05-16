# Course Outline

## 1. Fintech QA basics

Goal: understand how QA checks money-related user flows, not only HTTP responses.

Topics:
- fintech product risks;
- balances and operations;
- fees and rounding;
- negative API cases.

## 2. API testing foundation

Goal: learn how to test REST API manually and then automate checks.

Topics:
- HTTP methods;
- status codes;
- JSON payloads;
- Swagger and Postman;
- request and response validation.

## 3. Python and Pytest

Goal: build a simple API test project.

Topics:
- pytest basics;
- fixtures;
- parametrization;
- reusable API client helpers.

## 4. Fintech scenarios

Goal: test transfers, balances, fees and repeated requests.

Practice:
- account lookup;
- successful transfer;
- insufficient funds;
- fee calculation;
- repeated transfer with the same key.

## 5. Contract testing

Goal: check that API responses keep stable structure.

Topics:
- JSON Schema;
- required fields;
- field types;
- backward compatibility.

## 6. CI and reports

Goal: run tests automatically and collect reports.

Topics:
- GitHub Actions;
- Allure results;
- quality gates for pull requests.

## Final project

Student result: a GitHub repository with fintech API tests, CI workflow and clear README for portfolio use.
