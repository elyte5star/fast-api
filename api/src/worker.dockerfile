FROM python:3.12

WORKDIR /usr

COPY ["./", "./"]

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"

RUN pip install --upgrade pip && pip install poetry==1.6.1 

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

CMD ["python", "-u", "run_worker.py"]


