# 导入必要的库
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import pymysql
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['last_fetch_time'] = None

CORS(app)
csv_file_path = 'generated_data.csv'
model_lock = threading.Lock()  # 用于确保模型训练和预测的线程安全

# 训练模型的部分（用于示例）
data = pd.read_csv(csv_file_path)
X = data[['year', 'month', 'day', 'hour', 'minute', 'second']]  # 添加 'second'
y = data['temperature']
reg = RandomForestRegressor(n_estimators=100, random_state=45)
reg.fit(X, y)

# 定义变量来跟踪是否已进行预测
has_predicted = False


# 连接到数据库部分
def connect_to_database():
    conn = pymysql.connect(
        host='122.51.210.27',
        port=3306,
        user='1',
        password='cyh991103',
        database='数据'
    )
    return conn


# 从数据库获取新数据部分
def fetch_new_data_from_database(conn, last_fetch_time):
    cursor = conn.cursor()
    query = f"SELECT up_timestamp, temp FROM temp_hum WHERE up_timestamp > '{last_fetch_time}'"
    cursor.execute(query)

    data = cursor.fetchall()
    columns = ['up_timestamp', 'temperature']
    new_data = pd.DataFrame(data, columns=columns)

    new_data['up_timestamp'] = pd.to_datetime(new_data['up_timestamp'])
    new_data['year'] = new_data['up_timestamp'].dt.year
    new_data['month'] = new_data['up_timestamp'].dt.month
    new_data['day'] = new_data['up_timestamp'].dt.day
    new_data['hour'] = new_data['up_timestamp'].dt.hour
    new_data['minute'] = new_data['up_timestamp'].dt.minute
    new_data['second'] = new_data['up_timestamp'].dt.second  # 添加 'second'

    new_data.drop(['up_timestamp'], axis=1, inplace=True)

    new_data = new_data.dropna(subset=['temperature'])

    return new_data


# 存储数据到CSV文件部分
def save_data_to_csv(data, csv_file_path):
    data = data.dropna(subset=['temperature'])
    data.to_csv(csv_file_path, index=False, float_format='%.2f')


# 自动训练模型部分
def auto_train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    reg = RandomForestRegressor(n_estimators=100, random_state=45)
    reg.fit(X_train, y_train)
    return reg, X_test, y_test


# 后台线程用于定期训练模型
# def train_model_periodically():
#     while True:
#         time.sleep(3600)  # 每隔一小时训练一次
#         with model_lock:
#             global reg, csv_file_path
#             data = pd.read_csv(csv_file_path)
#             X = data[['year', 'month', 'day', 'hour', 'minute', 'second']]
#             y = data['temperature']
#             reg, X_test, y_test = auto_train_model(X, y)
#             score = reg.score(X_test, y_test)
#             print("模型得分:", score)
#
#
# # 启动后台线程
# model_thread = threading.Thread(target=train_model_periodically)
# model_thread.daemon = True
# model_thread.start()


# 预测温度部分
@app.route('/predict_temperature', methods=['POST'])
def predict_temperature():
    global has_predicted, reg, csv_file_path

    data = request.json
    future_year = data['year']
    future_month = data['month']
    future_day = data['day']
    future_hour = data['hour']
    future_minute = data['minute']
    future_second = data['second']

    future_data = pd.DataFrame({'year': [future_year], 'month': [future_month], 'day': [future_day],
                                'hour': [future_hour], 'minute': [future_minute], 'second': [future_second]})
    # 确保在训练和预测的时候模型状态一致
    with model_lock:
        future_temperature = reg.predict(future_data)

    conn = connect_to_database()

    if app.config['last_fetch_time'] is not None:
        new_data_from_database = fetch_new_data_from_database(conn, app.config['last_fetch_time'])
    else:
        new_data_from_database = fetch_new_data_from_database(conn, '1970-01-01 00:00:00')

    conn.close()

    if not new_data_from_database.empty:
        data = pd.read_csv(csv_file_path)
        data = pd.concat([data, new_data_from_database], ignore_index=True)
        save_data_to_csv(data, csv_file_path)

    app.config['last_fetch_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    has_predicted = True
    print("1")
    result = {"predicted_temperature": future_temperature[0]}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
