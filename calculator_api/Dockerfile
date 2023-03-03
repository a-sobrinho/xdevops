FROM python:3.10

ENV DJANGO_SETTINGS_MODULE calculator_api.settings

RUN pip install --upgrade pip && pip install poetry
WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false

RUN poetry install --no-root

CMD ["sh", "start.sh"]