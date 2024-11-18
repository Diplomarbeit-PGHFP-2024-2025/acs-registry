# ACS-Registry

## Installation

### Poetry

Poetry is a package manager for python

install it by following the [docs](https://python-poetry.org/docs/)

### just

just is a task running which is used in this project

[docs](https://github.com/casey/just)

## usage

install deps <br>
`just i`

install docker
[docs](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
afterwards
`sudo dockerd`

start MongoDB Docker <br>
`sudo just mongo`
---

start the ACS-Registry agent <br>
`just run`

start the testing station agent <br>
`just station`

start the testing car agent <br>
`just car`

### ruff

this project uses `ruff`

`just lint`

`just fix`
