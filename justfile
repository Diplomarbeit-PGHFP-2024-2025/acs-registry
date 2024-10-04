set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

alias i := install

install:
    poetry install

run:
    poetry run python src/__main__.py

car:
    poetry run python src/car.py

station:
    poetry run python src/station.py
