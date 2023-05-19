FROM python:3.10.0

WORKDIR /usr

COPY ["./", "./"]

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"

RUN pip install --upgrade pip && pip install poetry==1.4.2 

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-dev

CMD ["python", "-u", "run_worker.py"]


