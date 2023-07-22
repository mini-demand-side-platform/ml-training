![Build](https://github.com/mini-demand-side-platform/ml-training/workflows/build/badge.svg)
# ML Training
This is the machine learning training moudle in the [mini-demand-side-platform](https://github.com/mini-demand-side-platform/mini-demand-side-platform).

It trains the  click-through-rate (CTR) prediction model using historical data with [custom feature store service](https://github.com/mini-demand-side-platform/feature-store). Check the [notebooks](https://github.com/mini-demand-side-platform/research), if you want to see more detail of the modeling process.

Once the ML training server receives a training request, it initiates the process by querying the necessary data from a table generated from a custom feature store. The server then proceeds to train a logistic regression model using the acquired data. Once the training job is completed, the resulting model is securely written to object storage for the [ML server](https://github.com/mini-demand-side-platform/ml-serving).

## Usages
Training a new model.
```bash
curl -X 'POST' \
  'http://localhost:8001/model_training' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "feature_table_name": "top_10_features",
    "label_table_name": "ctr",
    "label_column_name": "was_click"
  }'
```
## Requirments
- Docker 
- Docker-compose 
- make
## Setup
If you want to run this training module on docker, please follow the instruction below.
#### 1. Active databases
```bash
git clone git@github.com:mini-demand-side-platform/databases.git
cd databases 
make run-all-with-example-data
```
#### 2. Run feature store
```bash
docker run -it --rm --network mini-demand-side-platform -p 8000:8000 \
	-e olap_host='postgresql' \
	-e cache_host='redis' \
	raywu60kg/feature-store
```

#### 3. Run ML training server 
```bash
docker run -it --rm --network mini-demand-side-platform \
    -p 8001:8001 \
	-e olap_host='postgresql' \
    -e object_storage_host='minio' \
	raywu60kg/ml-training
```