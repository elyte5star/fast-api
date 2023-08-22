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
SECRET_KEY=0c2214c33cc65769166ec5248bb0ec6a15e892ba649e36fefc5732d9c1ba469
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
MYSQL_ROOT_PASSWORD=54321
MYSQL_PASSWORD=54321
RABBIT_HOST=rabbitQ
RABBIT_PORT_NUMBER=5672
RABIT_PASSWORD=elyteRQ
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
