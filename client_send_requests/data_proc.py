txt_tables = []
# f = open("workload/workload-3", "r",encoding='utf-8')
f = open("bandwidth.txt", "r",encoding='utf-8')
line = f.readline()
columns = line.split()
# while line:
#     txt_data = eval(line) # 可将字符串变为元组
#     txt_tables.append(txt_data) # 列表增加
#     line = f.readline() # 读取下一行
# print(txt_tables)
float_list = list(map(float, columns))
print(float_list)