install:
	pip install -r requirements.txt

test:
	pytest

api:
	uvicorn src.finpay_sandbox.api:app --reload

allure:
	pytest --alluredir=allure-results
	allure serve allure-results
