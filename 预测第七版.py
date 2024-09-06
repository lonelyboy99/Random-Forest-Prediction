import pymysql
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime
import time


# 连接到云数据库
def connect_to_database():
    # 建立数据库连接
    conn = pymysql.connect(
        host='122.51.210.27',
        port=3306,
        user='1',
        password='cyh991103',
        database='数据'
    )
    return conn


# 从云数据库获取新数据，包括秒信息
def fetch_new_data_from_database(conn):
    cursor = conn.cursor()

    # 从数据库中选择数据
    query = "SELECT up_timestamp, temp FROM temp_hum"
    cursor.execute(query)

    # 获取数据并创建DataFrame
    data = cursor.fetchall()
    columns = ['up_timestamp', 'temperature']
    new_data = pd.DataFrame(data, columns=columns)

    # 处理时间戳列，添加年、月、日、时、分、秒等信息
    new_data['up_timestamp'] = pd.to_datetime(new_data['up_timestamp'])
    new_data['year'] = new_data['up_timestamp'].dt.year
    new_data['month'] = new_data['up_timestamp'].dt.month
    new_data['day'] = new_data['up_timestamp'].dt.day
    new_data['hour'] = new_data['up_timestamp'].dt.hour
    new_data['minute'] = new_data['up_timestamp'].dt.minute
    new_data['second'] = new_data['up_timestamp'].dt.second  # 添加秒特征

    # 删除原始时间戳列并删除缺失值
    new_data.drop(['up_timestamp'], axis=1, inplace=True)
    new_data = new_data.dropna(subset=['temperature'])
    return new_data


# 存储数据到CSV文件
def save_data_to_csv(data, csv_file_path):
    # 将数据保存到CSV文件
    data.to_csv(csv_file_path, index=False, float_format='%.2f')


# 自动训练模型
def auto_train_model(X, y):
    # 将数据划分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # 创建随机森林回归模型并进行训练
    reg = RandomForestRegressor(n_estimators=100, random_state=45)
    reg.fit(X_train, y_train)
    return reg, X_test, y_test


# 主程序
if __name__ == '__main__':
    csv_file_path = 'generated_data.csv'

    while True:
        # 从数据库获取新数据
        conn = connect_to_database()
        new_data_from_database = fetch_new_data_from_database(conn)
        conn.close()

        if not new_data_from_database.empty:
            # 读取已有的CSV文件并与新数据合并
            data = pd.read_csv(csv_file_path)
            data = pd.concat([data, new_data_from_database], ignore_index=True)

            # 将合并后的数据保存到CSV文件
            save_data_to_csv(data, csv_file_path)

            # 从合并后的数据中提取特征和目标变量
            X = data[['year', 'month', 'day', 'hour', 'minute', 'second']]
            y = data['temperature']

            # 自动训练模型
            reg, X_test, y_test = auto_train_model(X, y)
            score = reg.score(X_test, y_test)
            print("模型得分:", score)

        # 预测未来温度
        future_year, future_month, future_day, future_hour, future_minute, future_second = \
            map(int, input("请输入要预测的年份、月份、日期、小时、分钟和秒（以空格分隔）: ").split())
        future_data = pd.DataFrame({'year': [future_year], 'month': [future_month], 'day': [future_day],
                                    'hour': [future_hour], 'minute': [future_minute], 'second': [future_second]})

        future_temperature = reg.predict(future_data)

        date_time = datetime(year=future_year, month=future_month, day=future_day, hour=future_hour,
                             minute=future_minute, second=future_second)

        print("预测{}的温度: {:.2f}".format(date_time.strftime("%Y年%m月%d日 %H:%M:%S"), future_temperature[0]))