# FastAPI Gemini API

## Setup guide

https://medium.com/@ddias.olv/introduction-to-fastapi-with-poetry-a-practical-guide-to-creating-a-complete-api-very-simply-e736e8691010

## Install poetry

```bash
pip install poetry
```

## Install dependencies

```bash
poetry install
```

## Add dependencies

```bash
poetry add ...
```

## Run the API

```bash
poetry run python -m uvicorn src.main:app --reload
```

## Stop the API

## Deploy with Docker

### Build the Docker Image

```bash
docker build -t fastapi-gemini-api .
```

### Run the Docker Container

```bash
docker build -t fastapi-gemini-api .
```

### Stopping the Container

If you need to stop the running container, you can list all running containers with:

```bash
docker ps
```

Then, stop the container by its ID or name using:

```bash
docker stop <container_id_or_name>
```
