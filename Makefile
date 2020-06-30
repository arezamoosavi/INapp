deploy-registery:
	docker-compose -f docker-registery.yml up --build -d

clean-registery:
	docker-compose -f docker-registery.yml down -v

up-registry:
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker-build:
	docker build -t signapp .
	docker tag webapp 10.10.0.1:5000/signapp:v1

docker-run:
	docker run -p 3000:80 --name webapp -it --rm 10.10.0.1:5000/signapp:v1

docker-push:
	docker push 10.10.0.1:5000/signapp:v1

check-registry:
	curl -X GET http://10.10.0.1:5000/v2/webapp/tags/list

docker-bash:
	docker run --name webapp -it --rm 10.10.0.1:5000/signapp:v1 bash

del-minikube:
	minikube delete

init-minikube:
	minikube start --insecure-registry="10.10.0.1:5000"

create-dep:
	kubectl create deployment webapp --image=10.10.0.1:5000/signapp:v1 --dry-run=client -o=yaml > k8s/deployment.yaml

deploy-app:
	kubectl apply -f k8s/deployment.yaml

deploy-service:
	kubectl apply -f k8s/services.yaml

delete-all-deploy:
	kubectl delete -f k8s/
	minikube stop	