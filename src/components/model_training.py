from src.exception import CustomException
import os
import sys
from dataclasses import dataclass 
from catboost import CatBoostRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor 
from src.logger import logging 

from src.utils import save_object, evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_arr, test_arr):
        try:
            logging.info("Splitting training and test input data")
            X_train,y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            ) 

            # print(X_train.shape)
            # print(X_test.shape)
            # print(y_train.shape)
            # print(y_test.shape)
            
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "Ridge" : Ridge()
            }

            model_report: dict = evaluate_model(X_train = X_train,y_train = y_train,X_test = X_test,y_test = y_test, models = models)

            ## Getting the best model score
            best_model_score = max(sorted(model_report.values()))

            ## Getting the best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found", sys)
        
            logging.info("Found the best model")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = model
            )

            predicted = model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)