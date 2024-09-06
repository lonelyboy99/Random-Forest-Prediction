from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 读取数据
data = pd.read_csv('generated_data.csv')

# 特征选择：使用一年的某一天和某一年作为特征
X = data[['day_of_year', 'year']]
y = data['temperature']

# 数据集分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

# 创建线性回归模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# 预测测试集的温度
y_pred = reg.predict(X_test)
score = reg.score(X_test, y_test)

print('R2 score: ', score)
# 展示测试集的温度
results = pd.DataFrame({'Actual Temperature': y_test, 'Predicted Temperature': y_pred})
print(results)

# 假设input的格式为“day of year，year，temperature”
user_input = input("请输入日期的第几天, 年份, 温度（用逗号分隔）: ")
user_data = [float(x) for x in user_input.split(',')]

# 将用户输入数据附加到现有数据，如果已经存在相同数据则舍弃
if not data[(data['day_of_year'] == user_data[0]) & (data['year'] == user_data[1])].empty:
    print("已经在数据中出现，舍弃。")
else:
    new_data = pd.DataFrame(
        {'day_of_year': [user_data[0]], 'year': [user_data[1]], 'temperature': [user_data[2]]})  # 定义字典，包含三列
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv('generated_data.csv', index=False)

    # 重新拆分数据（如果需要）
    X = data[['day_of_year', 'year']]
    y = data['temperature']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

    # 重新训练模型
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    # 预测新数据的温度
    future_data = pd.DataFrame({'day_of_year': [user_data[0]], 'year': [user_data[1]]})
    future_temperature = reg.predict(future_data)

    # 将一年的某一天转化为日期
    date_of_prediction = datetime(year=int(user_data[1]), month=1, day=1) + pd.DateOffset(days=int(user_data[0]) - 1)

    print("预测{}的温度: {:.2f}".format(date_of_prediction.strftime("%Y年%m月%d日"), future_temperature[0]))

print("程序结束。")
