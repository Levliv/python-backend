FROM python:3.12

WORKDIR /shop_app

COPY .. /shop_app

RUN python -m pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "lecture_2.hw.shop_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
