from datetime import datetime

from fastapi import BackgroundTasks, FastAPI

from .config import (
    object_storage_server_info,
    olap_server_info,
)
from .data_pipeline import DataPipeline, PostgresDataPipeline
from .logger import get_logger
from .object_storage import MinioObjectStorage, ObjectStorage
from .train import SklearnTrain, Train

log = get_logger(logger_name="main")

app = FastAPI()
data_pipeline = PostgresDataPipeline(
    db_server_info=olap_server_info,
    feature_table_name="top_10_features",
    label_table_name="ctr",
    label_column_name="was_click",
)
train = SklearnTrain()
object_storage = MinioObjectStorage(db_server_info=object_storage_server_info)


def training_process(
    data_pipeline: DataPipeline,
    model_training: Train,
    object_storage: ObjectStorage,
):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    log.info("Start training at {}".format(dt_string))

    X_train, y_train = data_pipeline.get_training_data()
    X_test, y_test = data_pipeline.get_testing_data()
    model = model_training.model_fit(X_train=X_train, y_train=y_train)
    metrics = model_training.model_evaluate(model=model, X_test=X_test, y_test=y_test)
    model_training.model_save(
        object_storage=object_storage,
        bucket_name="models",
        training_time=dt_string,
        model=model,
        metrics=metrics,
    )
    log.info("Finished training")


@app.post("/model_training")
async def train_model(background_tasks: BackgroundTasks) -> bool:
    background_tasks.add_task(training_process, data_pipeline, train, object_storage)
    return True


@app.get("/health")
def health_check() -> bool:
    return True
