import io
import json
import pickle
from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, precision_recall_curve, roc_curve

from .logger import get_logger
from .object_storage import ObjectStorage

log = get_logger(logger_name="data_pipeline")


class Train(ABC):
    @abstractmethod
    def model_fit(self):
        pass

    @abstractmethod
    def model_evaluate(self):
        pass

    @abstractmethod
    def model_save(self):
        pass


class SklearnTrain(Train):
    def model_fit(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> BaseEstimator:
        # TODO put hyperparameter here
        clf = LogisticRegression(random_state=0).fit(X_train, y_train)
        return clf

    def model_evaluate(
        self, model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.DataFrame
    ) -> Dict[str, float]:
        predictions = model.predict_proba(X_test)[:, 1]

        # accuracy
        accuracy = model.score(X_test, y_test)

        # roc_auc
        fpr, tpr, _ = roc_curve(y_test, predictions)
        roc_auc = auc(fpr, tpr)

        # average_precision
        precision, recall, _ = precision_recall_curve(y_test, predictions)
        average_precision = auc(recall, precision)

        return {
            "accuracy": float(accuracy),
            "roc_auc": float(roc_auc),
            "average_precision": float(average_precision),
        }

    def model_save(
        self,
        object_storage: ObjectStorage,
        bucket_name,
        training_time,
        model: BaseEstimator,
        metrics: Dict[str, float],
    ) -> None:
        # save model
        model_pickle = pickle.dumps(model)
        model_stream = io.BytesIO(model_pickle)
        object_storage.save(
            bucket_name=bucket_name,
            object_name="model-{training_time}/model.pickle".format(
                training_time=training_time
            ),
            bytes_data=model_stream,
            data_length=len(model_pickle),
        )

        # save metrics
        metrics_json = json.dumps(metrics).encode("utf-8")
        metrics_stream = io.BytesIO(metrics_json)
        object_storage.save(
            bucket_name=bucket_name,
            object_name="model-{training_time}/metrics.json".format(
                training_time=training_time
            ),
            bytes_data=metrics_stream,
            data_length=len(metrics_json),
        )
