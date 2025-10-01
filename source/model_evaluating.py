import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# Overview:
# Split Train Test Data.
# Modeling:
# - Linear Regression.
# - Ridge Regression.
# - Random Forest Regressor.
# - XGBoost Regressor.
# Evaluation:
# - R2 Score.
# - MSE.
# Comparision.

def modeling_and_evaluating(df):
    # Split X (Attributes) and y (Price)
    X = df.drop(['Price'],axis = 1) 
    y = df['Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    # Linear Regression
    linear = LinearRegression(fit_intercept=False)
    linear.fit(X_train, y_train)
    
    # Evaluation
    y_test_pred1 = linear.predict(X_test)
    mse1 = mean_squared_error(y_test, y_test_pred1)
    print(">> R2 Score of Test Data: ",r2_score(y_test,y_test_pred1))
    print(">> Mean Squared Error:", mse1)
    
    # Ridge Regression
    ridge_reg = Ridge(alpha=1.0)
    ridge_reg.fit(X_train, y_train)
    # Evaluation
    y_test_pred2 = ridge_reg.predict(X_test)
    mse2 = mean_squared_error(y_test, y_test_pred2)
    print(">> R2 Score of Test Data: ",r2_score(y_test,y_test_pred2))
    print(">> Mean Squared Error:", mse2)

    # Random Forest Regression
    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=0)
    rf_regressor.fit(X_train, y_train)
    # Evaluation
    y_test_pred3 = rf_regressor.predict(X_test)
    mse3 = mean_squared_error(y_test, y_test_pred3)
    print(">> R2 Score of Test Data: ",r2_score(y_test,y_test_pred3))
    print(">> Mean Squared Error:", mse3)

    # XGBoost
    xgbm = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
    xgbm.fit(X_train, y_train)
    # Evaluation
    y_test_pred4 = xgbm.predict(X_test)
    mse4 = mean_squared_error(y_test, y_test_pred4)
    print(">> R2 Score of Test Data: ",r2_score(y_test,y_test_pred4))
    print('>> Mean Squared Error:',mse4)


    # Compare R2 Score
    r2 = [r2_score(y_test,y_test_pred1),r2_score(y_test,y_test_pred2),r2_score(y_test,y_test_pred3),r2_score(y_test,y_test_pred4)]
    model = ['LinearRegression','Ridge','RandomForest','XGBoost']
    
    # Visuallization
    plt.figure(figsize=(8, 6))
    plt.bar( model,r2, color='skyblue')
    plt.xlabel('Model')
    plt.ylabel('R2 score')
    plt.title('Model R2 score')
    plt.grid(True)
    plt.show()
    
    # Compare MSE
    mse = [mse1,mse2,mse3,mse4]
    # Visuallization
    plt.figure(figsize=(8, 6))
    plt.bar(model,mse, color='skyblue')
    plt.xlabel('Model')
    plt.ylabel('MSE')
    plt.title('Model MSE')
    plt.grid(True)
    plt.show()
