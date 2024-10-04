set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

alias i := install

install:
    poetry install

lint:
    poetry run ruff check
    poetry run ruff format --check

fix:
    poetry run ruff check --fix
    poetry run ruff format

run:
    poetry run python src/__main__.py

car:
    poetry run python src/car.py

station:
    poetry run python src/station.py
