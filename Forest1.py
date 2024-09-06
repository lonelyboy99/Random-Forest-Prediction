import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 读取数据
data = pd.read_csv('data.csv')

# 特征选择：使用一年的某一天和某一年作为特征
X = data[['day_of_year', 'year']]
y = data['temperature']

# 数据集分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40)

# 创建线性回归模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# # 随机森林训练模型
# reg = RandomForestRegressor(n_estimators=100).fit(X_train, y_train)

# 预测测试集的温度
y_pred = reg.predict(X_test)
score = reg.score(X_test, y_test)

print('R2 score: ', score)
# 展示测试集的温度
results = pd.DataFrame({'Actual Temperature': y_test, 'Predicted Temperature': y_pred})
print(results)

# 要预测的日期的特征：一年的某一天和某一年
future_day_of_year = int(input("请输入要预测的一年的某一天: "))
future_year = int(input("请输入要预测的年份: "))

# 使用模型进行预测
future_data = pd.DataFrame({'day_of_year': [future_day_of_year], 'year': [future_year]})
future_temperature = reg.predict(future_data)

# 打印预测结果
print("Predicted Temperature for Day {} of Year {}: {:.2f}".format(future_day_of_year, future_year, future_temperature[0]))
