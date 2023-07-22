package_name = ml-training
tag = 0.1.0

help:  
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

server-dev: ## start local dev server
	uvicorn ml_training.main:app --reload --port 8001

build-dev: ## build image
	docker build -t mini-demand-side-platform/ml-training:dev -f ./docker/Dockerfile .

run-dev: ## run image locally
	docker run -it --rm --network mini-demand-side-platform -p 8001:8001 \
	-e olap_host='postgresql' \
	-e object_storage_host='minio' \
	mini-demand-side-platform/ml-training:dev