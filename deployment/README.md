Starting the Deployment

- Project Setup:

  - Prerequisite

  ```
    openssl to create certificates
    Image registery..(Azure or DockerHub..etc) to pull images of application from.
    Intall helm and Kubectl. 
    Kubernetes cluster(Azure or GCP or AWS or minikube or microk8)
    Here I have used microk8s lightweight cluster on a local host(Linux).Follow these steps;
    sudo snap install microk8s --classic
    microk8s kubectl config view --raw > ~/.kube/config
    microk8s enable metallb:10.64.140.43-10.64.140.59 #These are fake IP addresses for the LoadBalancer
    microk8s enable hostpath-storage
    microk8s enable dns
    microk8s enable ingress
    sudo snap alias microk8s.kubectl kubectl
   


  ```

  - Create file api_secrets.env, ui_secrets.env and set values for the environment variables below and place them on the common folder:

      ```
      TOKEN_EXPIRE_MINUTES=50
      REFRESH_TOKEN_EXPIRE_MINUTES=43200
      HOST_URL=https://api.demo-elyte.test/
      CLIENT_URL=https://demo-elyte.test/
      MYSQL_HOST=db
      MYSQL_USER=userExample
      MYSQL_PORT=3306
      MYSQL_DATABASE=elyte
      MYSQL_ROOT_PASSWORD=54321
      MYSQL_PASSWORD=54321
      RABBIT_HOST=rabbitmq-cluster
      RABBITMQ_NODE_PORT=5672
      BACKEND_CORS_ORIGINS=["http://api.demo-elyte.test","https://api.demo-elyte.test", "https://demo-elyte.test", "http://*.demo-elyte.test", "http://localhost:8081", "http://demo-elyte.test", "http://demo-elyte.test:3001", "https://localhost:8081", "https://demo-elyte.test:443", "https://demo-elyte.test:4001"]
      RABBITMQ_DEFAULT_USER=rabbitUser
      RABBITMQ_DEFAULT_PASS=elyteRQ
      MSAL_ISSUER=https://login.microsoftonline.com/***************/v2.0
      MAIL_PASSWORD=****************
      SECURITY_PASSWORD_SALT=************
      GOOGLE_CLIENT_ID=**************.apps.googleusercontent.com
      MSAL_LOGIN_AUTHORITY=https://login.microsoftonline.com/********** */
      MSAL_CLIENT_ID=******
    

      ```
      VUE_API_URL=/api/v1/
      VUE_BASE_URL=https://demo-elyte.test/
      VITE_APP_WAIT_TIME=3000
      VUE_MAINTENANCE_MODE=false
      NGINX_PROXY_PASS=http://10.64.140.43:8081/ #backend url or IP addresss
      NGINX_PORT=8081

      ```
- Build and push images to image registery(I used a DockerHub).

  ```
  Go to the main application folder api/src and enter the following commands:
  docker login
  docker build -t docker.io/<YOURACCOUNT>/api:v1 -f ./backend.dockerfile . --no-cache
  docker push <YOURACCOUNT>/api:v1

  docker build -t docker.io/<YOURACCOUNT>/worker:v1 -f ./worker.dockerfile . --no-cache
  docker push <YOURACCOUNT>/worker:v1

  Go to the ui folder e-commerce and enter the following commands:

  docker build -t docker.io/<YOURACCOUNT>/vuejs:v1 -f ./frontend.dockerfile . --no-cache
  docker push <YOURACCOUNT>/vuej3:v1

  create regcred.yml that contains the secret to the registry

  apiVersion: v1
  data:
    .dockerconfigjson: ***********
  kind: Secret
  metadata:
    name: regcred
    namespace: demo
  type: kubernetes.io/dockerconfigjson
-  OR
```
  Create a namespace  with kubectl apply -f ns.yml from the /deployment/common directory.
  kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=<YOURUSERNAME> --docker-password=<YOURPASSWORD> --docker-email=<YOUREMAIL> --namespace demo

  kubectl -n demo get secret regcred --output=yaml


  ```

- Self signed certificate setup:

  - enter the common/openssl and enter the folowing command to create certificates

  ```
  chmod +x ssl.sh #make script executable
  ./ssl.sh demo-elyte.test

  cat demo-elyte.test.crt | base64
  cat demo-elyte.test.key | base64

  Use the values to create a TLS secret YML file.
  
  ```
- Deployment
  - enter the common folder and enter the folowing command to create deployment
  ```
    chmod +x deploy.sh #make script executable
    ./deploy.sh

  ```

  