
FROM python:3.10

# Copy only requirements to cache them in docker layer:
WORKDIR /usr

# Usage: COPY [from, from, from, to]
COPY ["./", "./"]

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"

RUN pip install --upgrade pip && pip install poetry==1.4.2 

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main


CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
