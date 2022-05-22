activate:
ifeq ($(OS),Windows_NT)
	PowerShell -NoExit ".\.venv\scripts\activate.ps1"
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		./.venv/Scripts/activate
	endif
	ifeq ($(UNAME_S),Darwin)
		./.venv/Scripts/activate
	endif
endif

deactivate:
ifeq ($(OS),Windows_NT)
	.\.venv\scripts\deactivate.bat
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		./.venv/Scripts/deactivate
	endif
	ifeq ($(UNAME_S),Darwin)
		./.venv/Scripts/deactivate
	endif
endif

freeze:
	python -m pip freeze > ./requirements.txt

test:
	python -m pytest --cov-config=.coveragerc -q ./tests/integration_tests.py --cov=src --cov=src/integrations --cov=src/ui

lint:
	python -m flake8 . --exit-zero --max-complexity=10

binary:
	python -m pyinstaller --onefile -w src/main.py

run:
	python src/main.py