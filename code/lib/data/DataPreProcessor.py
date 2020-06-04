import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataPreProcessor():
    def split_features(self, df, target_columns):
        targets_raw = df[target_columns]
        features_raw = df.drop(target_columns, axis=1)
        return features_raw, targets_raw

    def log_transform(self, df, skewed):
        df[skewed] = df[skewed].apply(lambda x: np.log(x + 1))

    def min_max_scaling(self, df, columns):
        scaler = MinMaxScaler()  # default=(0, 1)
        scaled_df = pd.DataFrame(df)
        scaled_df[columns] = scaler.fit_transform(scaled_df[columns])
        return scaled_df

    def one_hot_encode(self, df, prefix='feature'):
        return pd.get_dummies(df, prefix=prefix)


