set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

alias i := install

install:
    poetry install

lock:
    poetry lock

lint:
    poetry run ruff check
    poetry run ruff format --check

fix:
    poetry run ruff check --fix
    poetry run ruff format

run:
    poetry run python acs_registry/__init__.py

car:
    poetry run python acs_registry/stub/car.py

station:
    poetry run python acs_registry/stub/station.py

mongo:
    docker compose -f acs_registry/mongodb/compose.yml up