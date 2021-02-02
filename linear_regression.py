import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def get_data(data_file):
    features = []
    df = pd.read_csv(data_file, delimiter="\t")
    lines_of_code = df["lines_of_code"].tolist()
    classes = df["classes"].tolist()
    interfaces = df["interfaces"].tolist()
    inheritance = df["inheritance"].tolist()
    polymorphism = df["polymorphism"].tolist()
    labels = df["grade"].tolist()
    for i in range(len(df["project"].tolist())):
        feature = [lines_of_code[i], classes[i], interfaces[i], inheritance[i], polymorphism[i]]
        features.append(feature)
    features = np.asarray(features).astype("float32")
    labels = np.asarray(labels).astype("float32").reshape(len(labels), 1)
    return features, labels


features, labels = get_data("data.csv")

# split dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, shuffle=True)


k = 4  # split into 4 parts
num_val_samples = len(x_train) // k
all_rmse_scores = []

# k_fold validation
for i in range(k):
    print("Processing fold #", i)
    x_val = x_train[i * num_val_samples:(i + 1) * num_val_samples]
    y_val = y_train[i * num_val_samples:(i + 1) * num_val_samples]

    partial_train_data = np.concatenate(
        [x_train[:i * num_val_samples],
         x_train[(i + 1) * num_val_samples:]],
        axis=0)
    partial_train_targets = np.concatenate(
        [y_train[:i * num_val_samples],
         y_train[(i + 1) * num_val_samples:]],
        axis=0)

    lr = LinearRegression(normalize=True)
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_val)
    rmse = mean_squared_error(y_val, y_pred, squared=False)
    all_rmse_scores.append(rmse)

print(np.mean(all_rmse_scores))
