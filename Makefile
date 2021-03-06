start-registery:
	docker-compose -f docker-registery.yml up --build -d

clean-registery:
	docker-compose -f docker-registery.yml down -v

up-registry:
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker-build:
	docker build -t signapp .
	docker tag signapp 10.10.0.1:5000/signapp:v1

docker-run:
	docker run -p 3000:80 --name signapp -it --rm 10.10.0.1:5000/signapp:v1

docker-push:
	docker push 10.10.0.1:5000/signapp:v1

check-registry:
	curl -X GET http://10.10.0.1:5000/v2/signapp/tags/list

docker-bash:
	docker run --name signapp -it --rm 10.10.0.1:5000/signapp:v1 bash

del-minikube:
	minikube delete

init-minikube:
	minikube start --insecure-registry="10.10.0.1:5000"

create-dep:
	kubectl create deployment signapp --image=10.10.0.1:5000/signapp:v1 --dry-run=client -o=yaml > k8s/deployment.yaml

deploy-pg:
	kubectl apply -f k8s/postgre/

deploy-app:
	kubectl apply -f k8s/web/deployment.yaml

deploy-service:
	kubectl apply -f k8s/web/services.yaml

all-deploy:
	kubectl apply -f k8s/postgre/
	kubectl apply -f k8s/web/services.yaml
	kubectl apply -f k8s/web/deployment.yaml


delete-all-deploy:
	kubectl delete -f k8s/web/
	kubectl delete -f k8s/postgre/
	# minikube stop