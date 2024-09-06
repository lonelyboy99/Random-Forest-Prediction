import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 读入温度数据
data = pd.read_csv('generated_data.csv')

# 分离特征和标签
X = data[['day_of_year', 'year']]
y = data['temperature']

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 训练模型
reg = LinearRegression().fit(X_train, y_train)

# 预测结果
y_pred = reg.predict(X_test)

# 评估模型
score = reg.score(X_test, y_test)
print('R2 score: ', score)

