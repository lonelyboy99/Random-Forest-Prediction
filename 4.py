from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 读取数据
data = pd.read_csv('generated_data.csv')

# 特征选择：使用年、月、日、小时、分钟作为特征
X = data[['year', 'month', 'day', 'hour', 'minute']]
y = data['temperature']

# 数据集分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

# 创建线性回归模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# 预测测试集的温度
y_pred = reg.predict(X_test)
results = pd.DataFrame({'Actual Temperature': y_test, 'Predicted Temperature': y_pred})
print(results)

# 假设input的格式为“year,month,day,hour,minute,temperature”
user_input = input("请添加新数据，数据格式：年, 月, 日, 小时, 分钟, 温度（用逗号分隔）: ")
user_data = [float(x) for x in user_input.split(',')]

# 检查数据是否相同
if not ((data['year'] == user_data[0]) & (data['month'] == user_data[1]) & (data['day'] == user_data[2]) &
        (data['hour'] == user_data[3]) & (data['minute'] == user_data[4])).any():
    # 将用户输入数据附加到现有数据
    new_data = pd.DataFrame(
        {'year': [user_data[0]], 'month': [user_data[1]], 'day': [user_data[2]],
         'hour': [user_data[3]], 'minute': [user_data[4]], 'temperature': [user_data[5]]})  # 定义字典，包含六列
    data = pd.concat([data, new_data], ignore_index=True)  # 合并原始CSV文件和输入的数据
    data.to_csv('generated_data.csv', index=False)

# 重新拆分数据（如果需要）
X = data[['year', 'month', 'day', 'hour', 'minute']]
y = data['temperature']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

# 重新训练模型
reg = LinearRegression()
reg.fit(X_train, y_train)

# 要预测的日期和时间特征：年、月、日、小时、分钟
future_year = int(input("请输入要预测的年份: "))
future_month = int(input("请输入要预测的月份: "))
future_day = int(input("请输入要预测的日期: "))
future_hour = int(input("请输入要预测的小时: "))
future_minute = int(input("请输入要预测的分钟: "))

# 预测新数据的温度
future_data = pd.DataFrame({'year': [future_year], 'month': [future_month], 'day': [future_day],
                            'hour': [future_hour], 'minute': [future_minute]})
future_temperature = reg.predict(future_data)

# 构建日期时间对象
date_time = datetime(year=future_year, month=future_month, day=future_day, hour=future_hour, minute=future_minute)

print("预测{}的温度: {:.2f}".format(date_time.strftime("%Y年%m月%d日 %H:%M"), future_temperature[0]))

print("程序结束。")
