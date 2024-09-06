from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import paho.mqtt.client as mqtt
import json
import threading

# MQTT服务器和主题信息
mqtt_server = "122.51.210.27"
mqtt_topic = "temp_hum/emqx"

# 创建MQTT客户端
client = mqtt.Client()

# 全局变量用于存储模型
reg = RandomForestRegressor(n_estimators=100, random_state=45)
model_lock = threading.Lock()  # 用于确保模型训练的线程安全

# 回调函数，处理接收到的MQTT消息
def on_message(client, userdata, message):
    global reg  # 声明使用全局的模型变量
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)
    temperature = data.get("temp")

    # 检查数据是否相同
    is_duplicate = data.isin(data[['year', 'month', 'day', 'hour', 'minute']].values).all(1).any()

    if not is_duplicate:
        with model_lock:  # 获取模型训练锁
            # 将MQTT消息数据附加到现有数据
            new_data = pd.DataFrame({'year': [data['year']], 'month': [data['month']], 'day': [data['day']],
                                     'hour': [data['hour']], 'minute': [data['minute']], 'temperature': [temperature]})
            data = pd.concat([data, new_data], ignore_index=True)

            # 存储数据时，将数据格式设置为整数或带有两位小数的浮点数
            data.to_csv('generated_data.csv', index=False, float_format='%.2f')

            # 重新拆分数据
            X = data[['year', 'month', 'day', 'hour', 'minute']]
            y = data['temperature']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

            # 重新训练模型
            reg = RandomForestRegressor(n_estimators=100, random_state=45)
            reg.fit(X_train, y_train)

# 连接到MQTT服务器
client.connect(mqtt_server)
client.subscribe(mqtt_topic)

# 开始监听MQTT主题
client.loop_start()

# 用户输入要预测的日期和时间
future_year, future_month, future_day, future_hour, future_minute = \
    map(int, input("请输入要预测的年份, 月份, 日期, 小时和分钟（以空格分隔）: ").split())

# 创建一个占位符用于预测新数据的温度
future_data = pd.DataFrame({'year': [future_year], 'month': [future_month], 'day': [future_day],
                            'hour': [future_hour], 'minute': [future_minute]})

with model_lock:  # 获取模型训练锁
    future_temperature = reg.predict(future_data)

# 构建日期时间对象
date_time = datetime(year=future_year, month=future_month, day=future_day, hour=future_hour, minute=future_minute)

print("预测{}的温度: {:.2f}".format(date_time.strftime("%Y年%m月%d日 %H:%M"), future_temperature[0]))

# 程序结束
while True:
    pass
