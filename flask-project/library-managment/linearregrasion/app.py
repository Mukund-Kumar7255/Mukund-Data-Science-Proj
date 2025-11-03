from flask import *
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler

app=Flask(__name__)

with open('linear_model.pkl','rb') as f:
    saved_data=pickle.load(f)

scaler = StandardScaler()
minmax_scaler = MinMaxScaler()
train_data = {
    'feature1': [10, 20, 30, 45, 50, 60, 70, 80, 90, 100],
    'feature2': [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
}   
df_temp=pd.DataFrame(train_data)
scaler.fit(df_temp[['feature1','feature2']])
df_temp['combined_feature']=df_temp['feature1']+df_temp['feature2']
minmax_scaler.fit(df_temp[['combined_feature']])

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    features = [float(x) for x in request.form.values()]
    final_features = np.array(features).reshape(1, -1)
    prediction = saved_data.predict(final_features)[0]
    return render_template('index.html', prediction_text=f"Predicted Value: {round(prediction, 2)}")

if __name__ == "__main__":
    app.run(debug=True)
