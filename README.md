
# House Price Prediction

A Machine Learning project that predicts residential property prices using property characteristics such as location, BHK, bathrooms, area, furnishing status, and other features.

## Project Overview

The goal is to build and evaluate regression models that estimate house prices in Indian cities.

## Dataset

The dataset includes property information such as:
- City and locality type
- Property type and BHK
- Bathrooms and property area
- Floor number and property age
- Furnishing status, parking, and lift availability
- Distance to metro and city center

**Target variable:** `Price_INR_Lakhs`

## Machine Learning Workflow

1. Data loading and exploration
2. Exploratory Data Analysis (EDA)
3. Missing-value handling and preprocessing
4. Categorical feature encoding and numerical scaling
5. Train-test split
6. Training regression models
7. Model evaluation using MAE, RMSE, and R²
8. Hyperparameter tuning
9. Saving the trained model and generating predictions

## Models Evaluated

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Tuned Random Forest Regressor

## Evaluation Metrics

- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Squared Error
- **R²:** Coefficient of Determination

Actual model results will be added after verifying the final notebook outputs.

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Jupyter Notebook
- Joblib

## Project Structure

```text
House-Price-Prediction/
├── data/
├── models/
├── House_Price_Prediction.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

1. Clone or download this repository.
2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Open `House_Price_Prediction.ipynb` in Jupyter Notebook.
4. Run the notebook cells in order.

## Future Improvements

- Build an interactive house-price prediction app.
- Improve model performance through further experimentation.
- Allow users to enter property details and receive price estimates.
