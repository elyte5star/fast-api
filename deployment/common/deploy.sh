#! /bin/bash


echo "Creating namespace and secrets!"

kubectl apply -f ns.yml
kubectl apply -f ./openssl/tls.yml
kubectl apply -f regcred.yml
kubectl create secret generic api-secrets --namespace demo --from-env-file=api_secrets.env
kubectl create secret generic dashboard-secrets --namespace demo --from-env-file=ui_secrets.env

echo "Deploying Database!...."

kubectl apply -f ../db/db_network.yml
kubectl apply -f ../db/db_volume.yml
kubectl apply -f ../db/db_deployment.yml

sleep 30

echo "Oops! I fell asleep for a 30 seconds!"

echo "Deploying API!...."

kubectl apply -f ../api/api_network.yml
kubectl apply -f ../api/api_deployment.yml


sleep 40

echo "Oops! I fell asleep for a 40 seconds! Now Deploying Frontend!..."



kubectl apply -f ../ui/ui_network.yml
kubectl apply -f ../ui/ui_deployment.yml

sleep 40

echo "Oops! I fell asleep for a 40 seconds! Installing rabbitmq cluster operator using helm"

helm install --namespace demo rabbitmq bitnami/rabbitmq-cluster-operator --set clustering.forceBoot=true
sleep 30
echo "Slept for 30 seconds ..Now Deploying RabbitMQ cluster 1 replica set!...."
kubectl apply -f ../queue/rabbit_network.yml
kubectl apply -f ../queue/rabbit_pvc.yml
kubectl apply -f ../queue/rabbit_cluster.yml

sleep 60

echo "Check deployments"