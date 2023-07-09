from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, precision_recall_curve, roc_curve

from .logger import get_logger

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
            "accuracy": accuracy,
            "roc_auc": roc_auc,
            "average_precision": average_precision,
        }
