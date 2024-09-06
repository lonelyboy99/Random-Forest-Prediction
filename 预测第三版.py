from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 从CSV文件中读取数据
data = pd.read_csv('generated_data.csv')

# 选择特征：年、月、日、小时、分钟作为输入特征（X），温度作为目标（y）
X = data[['year', 'month', 'day', 'hour', 'minute']]
y = data['temperature']

# 将数据集分为训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 创建随机森林回归模型
reg = RandomForestRegressor(n_estimators=100, random_state=45)  # 可以调整n_estimators等参数，这个主要是设置森林树木的个数，树木数量越多，模型越精准
reg.fit(X_train, y_train)  # 训练模型

# 在测试集上预测温度
y_pred = reg.predict(X_test)
score = reg.score(X_test, y_test)  # 计算模型得分 就是那个R2分数 越靠近1,模型越好
print(score)

# 显示测试集上的实际温度和预测温度
results = pd.DataFrame({'Actual Temperature': y_test, 'Predicted Temperature': y_pred})
print(results)

# 假设input的格式为“year,month,day,hour,minute,temperature”
input_data = input("请添加新数据，数据格式：年, 月, 日, 小时, 分钟, 温度（用空格分隔），或者直接按回车键跳过: ")

if input_data:  # 如果用户提供了输入数据
    user_data = [float(x) for x in input_data.split()]  # 检测input_data字符串中的(空格)，拆分字符串，存入列表user_data中

    # 检查数据是否相同
    # 对data数据的每一列进行检查，保证每一列没有一样的
    if not ((data['year'] == user_data[0]) & (data['month'] == user_data[1]) & (data['day'] == user_data[2]) &
            (data['hour'] == user_data[3]) & (data['minute'] == user_data[4])).any():

        # 将用户输入数据附加到现有数据
        # year的数据是user_data的第一个数据，以此类推，创建了一个新的表格
        new_data = pd.DataFrame(
            {'year': [user_data[0]], 'month': [user_data[1]], 'day': [user_data[2]],
             'hour': [user_data[3]], 'minute': [user_data[4]], 'temperature': [user_data[5]]})
        # 将原始data数据和new_data合并，data数据是代码第7行提取的
        data = pd.concat([data, new_data], ignore_index=True)  # 合并原始CSV文件和输入的数据

        # 存储数据时，将数据格式设置为整数或带有两位小数的浮点数，存到generated_data.csv
        data.to_csv('generated_data.csv', index=False, float_format='%.2f')

        # 重新拆分数据
        X = data[['year', 'month', 'day', 'hour', 'minute']]
        y = data['temperature']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # 重新训练模型
        reg = RandomForestRegressor(n_estimators=100, random_state=45)  # 可以调整n_estimators等参数
        reg.fit(X_train, y_train)

# 要预测的日期和时间特征：年、月、日、小时、分钟
future_year, future_month, future_day, future_hour, future_minute = \
    map(int, input("请输入要预测的年份,月份,日期,小时和分钟（以空格分隔）: ").split())

# 预测新数据的温度
# future_year，month，day，hour，minute都对应键入的值
future_data = pd.DataFrame({'year': [future_year], 'month': [future_month], 'day': [future_day],
                            'hour': [future_hour], 'minute': [future_minute]})
future_temperature = reg.predict(future_data)

# 构建日期时间对象
date_time = datetime(year=future_year, month=future_month, day=future_day, hour=future_hour, minute=future_minute)

# 输出预测温度并将预测的数据按照时间格式排列出来比如2023年11月1日 8:40
print("预测{}的温度: {:.2f}".format(date_time.strftime("%Y年%m月%d日 %H:%M"), future_temperature[0]))
