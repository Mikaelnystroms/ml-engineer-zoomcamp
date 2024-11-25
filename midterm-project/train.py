import os
import subprocess
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
import joblib

def load_data(filepath):
    """Load and prepare the wine quality dataset"""
    df = pd.read_csv(filepath, delimiter=";")
    # Clean column names: replace spaces with underscores and make lowercase
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    X = df.drop('quality', axis=1)
    y = df['quality']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def create_model_pipelines():
    """Create dictionary of model pipelines"""
    return {
        'Linear Regression': Pipeline([
            ('scaler', StandardScaler()),
            ('model', LinearRegression())
        ]),
        'Random Forest': Pipeline([
            ('model', RandomForestRegressor(random_state=42))
        ]),
        'XGBoost': Pipeline([
            ('model', xgb.XGBRegressor(random_state=42, eval_metric='rmse'))
        ])
    }

def get_param_grids():
    """Define hyperparameter search spaces"""
    return {
        'Random Forest': {
            'model__n_estimators': [100, 200, 300],
            'model__max_depth': [10, 20, 30],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 2, 4]
        },
        'XGBoost': {
            'model__n_estimators': [100, 200, 300],
            'model__max_depth': [3, 5, 7],
            'model__learning_rate': [0.01, 0.1, 0.3],
            'model__subsample': [0.8, 0.9, 1.0]
        }
    }

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train models and return the best one"""
    pipelines = create_model_pipelines()
    param_grids = get_param_grids()
    best_models = {}

    for name, pipeline in pipelines.items():
        print(f"Evaluating {name}...")
        scores = cross_val_score(pipeline, X_train, y_train, cv=5, 
                               scoring='neg_mean_squared_error', n_jobs=-1)
        rmse_scores = np.sqrt(-scores)
        print(f"Mean CV RMSE: {rmse_scores.mean():.4f} (+/- {rmse_scores.std():.4f})")
        
        param_grid = param_grids.get(name)
        if param_grid:
            grid_search = RandomizedSearchCV(
                estimator=pipeline,
                param_distributions=param_grid,
                n_iter=20,
                cv=5,
                scoring='neg_mean_squared_error',
                n_jobs=-1,
                random_state=42
            )
            grid_search.fit(X_train, y_train)
            best_models[name] = grid_search.best_estimator_
            print(f"Best Params for {name}: {grid_search.best_params_}")
        else:
            pipeline.fit(X_train, y_train)
            best_models[name] = pipeline

    # Select best model
    best_model_name = min(best_models, key=lambda name: np.mean(np.sqrt(-cross_val_score(
        best_models[name], X_train, y_train, cv=5, 
        scoring='neg_mean_squared_error', n_jobs=-1))))
    
    return best_models[best_model_name], best_model_name

def main():    
    data_path = "data/winequality-red.csv"
    if not os.path.exists(data_path):
        print("Downloading wine quality dataset...")
        subprocess.run(["wget", "https://archive.ics.uci.edu/static/public/186/wine+quality.zip"])
        subprocess.run(["unzip", "wine+quality.zip"])
        # Move file to expected location
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        subprocess.run(["mv", "winequality-red.csv", data_path])
        # Clean up zip file
        subprocess.run(["rm", "wine+quality.zip"])
    # Load and split data
    X_train, X_test, y_train, y_test = load_data(data_path)
    
    # Train and get best model
    final_model, best_model_name = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Evaluate on test set
    test_predictions = final_model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
    test_mae = mean_absolute_error(y_test, test_predictions)
    test_r2 = r2_score(y_test, test_predictions)

    print(f"\nBest Model: {best_model_name}")
    print("\nTest Set Performance:")
    print(f"RMSE: {test_rmse:.4f}")
    print(f"MAE: {test_mae:.4f}")
    print(f"R² Score: {test_r2:.4f}")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    model_path = 'models/wine_quality_model.joblib'
    joblib.dump(final_model, model_path)
    print(f"\nModel saved to {model_path}")
    
    return final_model

if __name__ == "__main__":
    main()