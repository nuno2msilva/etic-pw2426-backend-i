FROM python:3.12-slim

WORKDIR /workspace

COPY . .

RUN pip install poetry

RUN poetry install --quiet --no-interaction

ENTRYPOINT [ "poetry" , "run" , "uvicorn" ]

CMD [ "session_12.main:api" , "--host" , "0.0.0.0" ]