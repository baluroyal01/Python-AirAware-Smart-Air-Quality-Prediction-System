🌬️ Air Quality Prediction System
  This repository contains a Machine Learning system that predicts the Air Quality Index (AQI) based on historical pollutant      data. The model is trained to identify patterns in chemical concentrations to provide a numerical AQI value, helping to         monitor urban pollution levels.
📌 Project OverviewAir pollution is a significant environmental risk to health. This project uses historical data of various     pollutants to build a predictive model. By analyzing the correlation between pollutants like $PM_{2.5}$ and $NO_x$, the         system can forecast air quality with high precision.
Key Objectives:
 Perform Exploratory Data Analysis (EDA) on air quality variables.
 Handle missing environmental data using mean/median imputation.
 Train and evaluate a Random Forest Regressor for AQI estimation.
🛠️ Tech Stack:
  Language: Python 3.x
  Data Science: Pandas, NumPy
  Machine Learning: Scikit-Learn
  Visualization: Matplotlib, Seaborn
📊 Dataset & Model DetailsDataset Source: Kaggle: 
  Air Quality Data in India (2015-2020)
  Target Variable: AQIFeatures: $PM_{2.5}, PM_{10}, NO, NO_2, NO_x, NH_3, CO, SO_2, O_3
  Model: Random Forest Regressor (chosen for its ability to handle non-linear relationships in environmental data).
  
