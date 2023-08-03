# 打开.log文件
with open('bandwidthdata/report_car_0001.log', 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 使用空格分割每行内容
        columns = line.split()
        # 检查是否有足够的列数
        if len(columns) >= 6:
            # 获取指定列的值
            band_width = float(columns[4]) / float(columns[5]) / 1024 / 1024 * 1000
            with open('bandwidth.txt', 'a') as f:
                f.write(str(band_width) + " ")
            # # 打印指定列的值
            # print(column_value)
