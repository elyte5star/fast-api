Starting the project

- Project Setup:

  - Clone project with

  ```
  git clone git@github.com:elyte5star/fast-api-queue.git
  ```

  - Create file api.env and set values for the environment variables below:

  ```
  PYTHONUNBUFFERED=x
  GOOGLE_CLIENT_ID=xxxxxxx-xxxxxxxx.apps.googleusercontent.com
  GOOGLE_CLIENT_SECRET=xxxx-xxx-xxxxx
  GOOGLE_DISCOVERY_URL=xxxxxxxx
  ALGORITHM=xxxx
  SECRET_KEY=xxxxxxxx
  TOKEN_EXPIRE_MINUTES=xxx
  HOST_URL=http://localhost:8080
  MYSQL_HOST=xxxxx
  MYSQL_USER=xxxxx
  MYSQL_DATABASE=xxxxxx
  MYSQL_ROOT_PASSWORD=xxxxxx
  MYSQL_PASSWORD=xxxxx
  ```

- Docker setup run:

  - Run migrations with

  ```
  docker-compose up db

  docker-compose up rabbitQ
  
  docker-compose build api

  docker-compose build worker
  ```

  - start server with

  ```
  docker-compose up api

  docker-compose up worker

  ```
