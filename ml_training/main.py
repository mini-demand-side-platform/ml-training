from datetime import datetime
from typing import Optional

from fastapi import BackgroundTasks, FastAPI
from minio import Minio

from .config import (
    data_pipeline_method,
    minio_server_info,
    model_saver_method,
    olap_server_info,
    train_method,
)
from .data_pipeline import DataPipeline, PostgresDataPipeline
from .logger import get_logger
from .model_saver import MinioModelSaver, ModelSaver
from .train import SklearnTrain, Train

log = get_logger(logger_name="main")

app = FastAPI()


def training_process(
    data_pipeline: DataPipeline, model_training: Train, model_saver: ModelSaver
):
    X_train, y_train = data_pipeline.get_training_data()
    X_test, y_test = data_pipeline.get_testing_data()
    model_training.model_fit(X_train=X_train, y_train=y_train)


@app.post("/model_training")
async def train_model(background_tasks: BackgroundTasks) -> bool:
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    log.info("Start training at {}".format(dt_string))
    try:
        if data_pipeline_method == "postgres":
            pdp = PostgresDataPipeline(db_server_info=olap_server_info)

            X_train, y_train = pdp.get_training_data()
            X_test, y_test = pdp.get_testing_data()

        else:
            log.error(
                "Not support data_pipeline_method: {}".format(data_pipeline_method)
            )
            return False
    except Exception as e:
        log.error("Data Pipeline error: {}".format(e))
        return "Data pipeline error: {}".format(e)
    try:
        if train_method == "sklearn":
            skt = SklearnTrain(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
            )
            model = skt.model_fit()
            model_metrics = skt.model_evaluate(model=model)
        else:
            return "Not support train_method: {}".format(train_method)
    except Exception as e:
        log.error("Train model error: {}".format(e))
        return "Model training error {}".format(e)

    try:
        if model_saver_method == "minio":
            minio_client = Minio(
                minio_server_info["uri"],
                minio_server_info["access_key"],
                minio_server_info["secret_key"],
                secure=False,
            )
            mms = MinioModelSaver(minio_client=minio_client)
            mms.save(
                model=model,
                model_metrics=model_metrics,
                bucket_name="model-" + dt_string,
            )
        else:
            return "Not support model_saver_method: {}".format(model_saver_method)
    except Exception as e:
        log.error("Save model error: {}".format(e))
        return "Save model error {}".format(e)
    return {"model": True}


@app.get("/model_list/")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/serving_model")
def update_serving_model(model_bucket_name: str):
    return {"hi": "there"}


@app.get("/health")
def health_check() -> bool:
    return True
