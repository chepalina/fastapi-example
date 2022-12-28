FROM docker-hosted.artifactory.tcsbank.ru/dwh-core/python/poetry/3.9:1.6.3 as app

RUN poetry install --no-dev
COPY . .

FROM app as tests

RUN poetry install
