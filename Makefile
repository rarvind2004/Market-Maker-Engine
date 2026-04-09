install:
	pip install -e .[dev]

backtest:
	python scripts/run_backtest.py

api:
	uvicorn market_maker.api.app:app --reload

test:
	pytest
