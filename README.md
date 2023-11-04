Starting the project

- Project Setup:

  - Clone project with

  ```
  git clone git@github.com:elyte5star/fast-api.git
  ```

  - Create file api.env and set values for the environment variables below:

  ```
  
  TOKEN_EXPIRE_MINUTES=50
  REFRESH_TOKEN_EXPIRE_MINUTES=43200
  HOST_URL=http://localhost:8000/
  CLIENT_URL=http://localhost:9000/
  BACKEND_CORS_ORIGINS='["https://demo-elyte.com", "http://*.demo-elyte.com", "http://localhost", "http://localhost:9000"]'
  MYSQL_HOST=db
  MYSQL_USER=userExample
  MYSQL_PORT=3306
  MYSQL_DATABASE=elyte
  MYSQL_ROOT_PASSWORD=54321
  MYSQL_PASSWORD=54321
  RABBIT_HOST=rabbitQ
  RABBITMQ_NODE_PORT=5672
  RABBITMQ_DEFAULT_USER=rabbitUser
  RABBITMQ_DEFAULT_PASS=elyteRQ
  MAIL_PASSWORD=********************
  SECURITY_PASSWORD_SALT=************
  GOOGLE_CLIENT_ID=*************.apps.googleusercontent.com
  MSAL_CLIENT_ID=*****************************
  MSAL_ISSUER=https://login.microsoftonline.com/***************/v2.0
  MSAL_LOGIN_AUTHORITY=https://login.microsoftonline.com/**********/

  ```

- Docker setup run:

  - Run migrations with

  ```
  docker-compose up db

  docker-compose up rabbitQ
  
  docker-compose build api

  docker-compose build worker
  ```

  - start server with and worker

  ```
  docker-compose up api

  docker-compose up worker

  ```
