# 创建一个三维空数组
arr = []

while True:
    # 输入数据
    input_data = input("请输入day_of_year,year,temperature: ")
    if input_data.lower() == 'q':
        break

    # 尝试解析输入数据为三维坐标
    try:
        day_of_year, year, temperature = map(int, input_data.split(','))
        # 判断坐标是否已经在数组中出现
        is_duplicate = False
        for item in arr:
            if (day_of_year, year, temperature) == item:
                is_duplicate = True
                break

        if not is_duplicate:
            # 如果没有出现，将坐标存入数组并打印
            arr.append((day_of_year, year, temperature))
            print(f"day_of_year:{day_of_year}，year:{year}，temperature:{temperature}已存入数组，当前数组为: {arr}")
        else:
            # 如果已经出现，舍弃该坐标
            print(f"已经在数组中出现，舍弃。")
            print(arr)
    except ValueError:
        print("无效输入，请按照格式输入。")

print("程序结束。")
print(arr)

