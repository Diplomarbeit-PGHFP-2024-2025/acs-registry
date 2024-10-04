set shell := ["powershell.exe", "-c"]

run:
    poetry run python src/__main__.py

car:
    poetry run python src/car.py

station:
    poetry run python src/station.py
