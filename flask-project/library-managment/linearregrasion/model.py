import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
# We are adding mean_absolute_error and r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = {
    'feature1': [10, 20, 30, np.nan, 50, 60, 70, 80, 90, 100],
    'feature2': [15, 25, 35, 45, 55, 65, 75, np.nan, 95, 105],
    'feature_cat': ['A', 'B', 'A', 'C', 'B', 'B', 'A', 'C', 'A', 'B'],
    'garbage_val': [1, 2, -999, 4, 5, 6, 7, 8, -999, 10],
    'target': [110, 125, 140, 155, 170, 185, 200, 215, 230, 245]
}
df = pd.DataFrame(data)
df['feature1'] = df['feature1'].fillna(df['feature1'].mean())
df['feature2'] = df['feature2'].fillna(df['feature2'].median())

# replace garbage value by mode
clean_mode=df[df['garbage_val']!=-999]['garbage_val'].mode()[0]
df['garbage_val']=df['garbage_val'].replace(-999,clean_mode)

# feature engineering
df['Combined_feature']=df['feature1']+df['feature2']

# one hot encoding
df=pd.get_dummies(df, columns=['feature_cat'], drop_first=True)

# feature standardization
scaler=StandardScaler()
df[['feature1','feature2']]=scaler.fit_transform(df[['feature1','feature2']])

# Normalization
minmax_scaler=MinMaxScaler()
df['Combined_feature']=minmax_scaler.fit_transform(df[['Combined_feature']])

# Applying linear regression
X=df.drop('target',axis=1)
y=df['target']

X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.2,random_state=42)

model=LinearRegression()
model.fit(X_train,y_train)

with open('linear_model.pkl', 'wb') as f:
    pickle.dump(model, f)