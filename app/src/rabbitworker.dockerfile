FROM --platform=linux/amd64 python:3.10.0

# Copy only requirements to cache them in docker layer:
WORKDIR /usr/src

COPY [ "pyproject.toml", "./"]

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"

RUN pip install --upgrade pip && pip install poetry==1.1.12

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Run the application:
CMD ["python", "-u", "run_worker.py"]

EXPOSE 8080 5678