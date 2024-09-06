import random

# 初始化一个空列表，用于存储生成的数据
data = []

# 循环生成1000份数据
for _ in range(1000):
    day_of_year = random.randint(1, 365)  # 一年中的第几天，假设是365天的年份
    year = random.randint(2021, 2023)  # 随机年份，可以根据需要进行修改
    temperature = round(random.uniform(0, 40), 1)  # 随机生成温度，可以根据需要进行修改

    # 将生成的数据添加到列表中
    data.append((day_of_year, year, temperature))

# 打印前10行数据，以检查生成结果
for row in data[:10]:
    print(','.join(map(str, row)))

# 将生成的数据保存到文件
with open('data.csv', 'w') as file:
    file.write('day_of_year,year,temperature\n')
    for row in data:
        file.write(','.join(map(str, row)) + '\n')
