# NDS price optimal

> Calculating optimal price with and without NDS

## Prerequisites

- [Git][g];
- [uv][u];
- Docker Compose, build-in with [Docker Desktop][d].

[g]: https://git-scm.com/
[u]: https://docs.astral.sh/uv/
[d]: https://www.docker.com/products/docker-desktop/

## Preparation

### Clone

```
git clone https://github.com/nsvetlana/nds-price-optimal.git
```

```
cd nds-price-optimal
```


## Run

### Tests via Docker Compose

```
docker compose up
```


## Development

### Install Python

```
uv python install
```


### Install and update dependencies

```
uv sync
```


### Run tests

```
pytest
```