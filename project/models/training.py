"""
Class to prepare the unioned gameweeks for modelling.
"""
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def split_and_scale(predictors, labels, scaler, numerical_columns, test_size=0.2, stratify=None, random_state=1):
    """
    performs a train-test split and then transforms the numerical columns in both the training and test sets using a
    feature scaler that is fitted to the training set
    the feature names are therefore the same as the dummified predictors columns.
    :param predictors: pandas.core.frame.DataFrame
    :param labels: pandas.core.frame.Series
    :param scaler: sklearn.preprocessing._data.Transformer
    :param numerical_columns: list
    :param test_size: float
    :param stratify: list
    :param random_state: int
    :return: np.array, np.array, list, list, sklearn.preprocessing._data.Transformer
    """
    x_train, x_test, y_train, y_test = train_test_split(predictors, labels, test_size=test_size, stratify=stratify,
                                                        random_state=random_state)
    transformer = ColumnTransformer([('numerical', scaler, numerical_columns)], remainder='passthrough')
    x_train = transformer.fit_transform(x_train)
    x_test = transformer.transform(x_test)
    return np.array(x_train), np.array(x_test), y_train, y_test, transformer


class Training:
    def __init__(self, dataframe):
        """
        :param dataframe: pandas.core.frame.DataFrame
        """
        self.labels = dataframe.pop("shift_total_points_range")
        self.training_data = dataframe

        self.categorical_columns = ["season", "name", "position", "plays_for", "shift_opponent", "shift_month_of_match",
                                    "shift_time_of_match"]
        self.numerical_columns = [col for col in dataframe.columns if col not in self.categorical_columns]

    def dummify_categories(self):
        """
        dummify the categorical columns in the training data
        :return: None
        """

        self.training_data = pd.get_dummies(self.training_data, columns=self.categorical_columns)

    def split_into_train_and_test(self):
        """
        split the training data into the test set and the train set for modelling.
        :return: np.array, np.array, list, list, sklearn.preprocessing._data.Transformer
        """
        return split_and_scale(self.training_data, self.labels, MinMaxScaler(), self.numerical_columns,
                               stratify=self.labels)
