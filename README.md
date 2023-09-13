Starting the project

- Project Setup:

  - Clone project with

  ```
  git clone git@github.com:elyte5star/fast-api-queue.git
  ```

  - Create file api.env and set values for the environment variables below:

  ```
  DEBUG=1
  ALGORITHM=HS256
  SECRET_KEY=***********************************************************
  TOKEN_EXPIRE_MINUTES=50
  REFRESH_TOKEN_EXPIRE_MINUTES=43200
  HOST_URL=http://localhost:8000/
  CLIENT_URL=http://localhost:9000
  HOST_PORT=8000
  API_HOST=http://api
  HASH_CODING=utf-8
  HASH_LENGTH=16
  HASH_ROUNDS=10
  MYSQL_HOST=db
  MYSQL_USER=userExample
  MYSQL_PORT=3306
  MYSQL_DATABASE=elyte
  MYSQL_ROOT_PASSWORD=**************
  MYSQL_PASSWORD=*******
  RABBIT_HOST=****
  RABBIT_PORT_NUMBER=5672
  RABIT_PASSWORD=*****
  RABBIT_QNAME='["SEARCH", "BOOKING", "LOST_ITEM"]'
  MAIL_USERNAME=**********
  MAIL_PASSWORD=*********
  MAIL_FROM=example@mail.com
  MAIL_PORT=587
  MAIL_SERVER=smtp.gmail.com
  MAIL_FROM_NAME="E-COMMERCE APPLICATION "
  MAIL_STARTTLS=true
  MAIL_SSL_TLS=false
  USE_CREDENTIALS=true
  VALIDATE_CERTS=true
  SECURITY_PASSWORD_SALT=***********
  GOOGLE_CLIENT_ID=***********.apps.googleusercontent.com
  GOOGLE_CLIENT_SECRET=***********
  MSAL_CLIENT_ID=*************
  MSAL_ISSUER=https://login.microsoftonline.com/*******/v2.0
  MSAL_LOGIN_AUTHORITY=https://login.microsoftonline.com/*****

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
