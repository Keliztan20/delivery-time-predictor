import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ---------------------- 1. Load & Split Dataset ----------------------
def load_and_split_data(filepath, target_column='Time_taken', test_size=0.2, encoding='latin-1'):
    df = pd.read_csv(filepath, encoding=encoding)
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)
    train_df.to_csv('assets/train.csv', index=False)
    test_df.to_csv('assets/test.csv', index=False)
    return train_df, test_df


# ---------------------- 2. Prepare LightGBM Datasets ----------------------
def prepare_lgb_datasets(train_df, test_df, target_column='Time_taken'):
    X_train = train_df.drop(columns=[target_column])
    y_train = train_df[target_column]
    X_test = test_df.drop(columns=[target_column])
    y_test = test_df[target_column]
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    return X_train, y_train, X_test, y_test, train_data, test_data


# ---------------------- 3. Train Model ----------------------
def train_model(train_data, test_data, params=None):
    if params is None:
        params = {
            'objective': 'regression',
            'metric': ['mae', 'mse'],
            'boosting_type': 'gbdt',
            'num_leaves': 255,
            'learning_rate': 0.05,
            'max_depth': 16,
            'min_data_in_leaf': 12,
            'random_state': 42,
            'feature_fraction': 0.5,
            'verbosity': -1,
        }

    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[train_data, test_data],
        valid_names=['train', 'test'],
        callbacks=[
            lgb.early_stopping(stopping_rounds=100, verbose=True),
            lgb.log_evaluation(100)
        ]
    )
    return model


# ---------------------- 4. Evaluation Metrics ----------------------
def calculate_metrics(y_true, y_pred, set_name='Set'):
    return {
        'Dataset': set_name,
        'MAE': mean_absolute_error(y_true, y_pred),
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'R2': r2_score(y_true, y_pred)
    }


# ---------------------- 5. Run Pipeline ----------------------
def main():
    print("Loading and splitting data...")
    train_df, test_df = load_and_split_data("assets\Final.csv")

    print("Preparing datasets...")
    X_train, y_train, X_test, y_test, train_data, test_data = prepare_lgb_datasets(train_df, test_df)

    print("Training model...")
    model = train_model(train_data, test_data)

    print("Generating predictions and evaluating...")
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    metrics = [
        calculate_metrics(y_train, train_pred, 'Training'),
        calculate_metrics(y_test, test_pred, 'Test')
    ]

    metrics_df = pd.DataFrame(metrics)
    print("\nPerformance Metrics:")
    print(metrics_df.to_markdown(index=False))

    print("Saving model to 'Delivery_time_predictor.h5'...")
    model.save_model('assets/Delivery_time_predictor.h5', num_iteration=model.best_iteration)
    print("Done.")


# ---------------------- 6. Entry Point ----------------------
if __name__ == '__main__':
    main()
