import sqlite3


def fetch_new_data_from_database():
    # 连接到数据库
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # 查询数据库中的新数据，可以根据需要自定义查询条件
    query = "SELECT year, month, day, hour, minute, temperature FROM data_table WHERE data_status = 'new'"
    cursor.execute(query)

    # 获取查询结果并将其存储到DataFrame
    data = cursor.fetchall()
    columns = ['year', 'month', 'day', 'hour', 'minute', 'temperature']
    new_data = pd.DataFrame(data, columns=columns)

    # 更新数据库中的数据状态（例如，将数据标记为已处理）
    update_query = "UPDATE data_table SET data_status = 'processed' WHERE data_status = 'new'"
    cursor.execute(update_query)
    conn.commit()

    # 关闭数据库连接
    conn.close()

    return new_data
