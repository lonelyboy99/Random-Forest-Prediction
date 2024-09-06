# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 训练模型的部分（用于示例）
data = pd.read_csv('generated_data.csv')
X = data[['day_of_year', 'year']]
y = data['temperature']
reg = LinearRegression()
reg.fit(X, y)

@app.route('/predict_temperature', methods=['POST'])
def predict_temperature():
    data = request.json
    future_day_of_year = data['day_of_year']
    future_year = data['year']

    # 使用训练好的模型进行预测
    future_data = pd.DataFrame({'day_of_year': [future_day_of_year], 'year': [future_year]})
    predicted_temperature = reg.predict(future_data)[0]

    # 返回预测结果
    result = {"predicted_temperature": predicted_temperature}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
