# 先不要想别的，把伪代码实现了再说
# 先假定R和B和t_slo都是常量
# 一行一行实现，不着急，但绝对要自己一个人弄出来，不要去求人

import math
import glob


# 6.6：serverless用cpu推的太慢了，如果slo取值0.4，batch无法超过1，因为等待时间就很长
#       并且发出去的还是给serverless的 要换成edge的再完善一下
# 6.21：已经解决，问题出在下标标错了，现在serverless上batch在5以内的基本上都有


# 读取边缘端、serverless测试得到的数据
# 已完成拟合，直接用取拟合函数代替
def fitFunEdge(b):
    l = 0.008165 * b + 0.04234
    return l


def fitFunServerless(b, m):
    # l = 0.1661 * b - 9.966e-05 * m + 0.399
    l = 0.141 * b - 8.806e-06 * m + 0.225
    return l


def fitTransTime(b, B):
    t = (200 / 1024 * b) / B  # 这里取测得带宽平均值2.857MB/s，实在不好拿到实时网速
    return t


# # 获取带宽数据 算法在进行推演时应该隔几分钟检查一次
# def get_band_width():
#     ret = []
#     file_list = sorted(glob.glob("bandwidthdata/*.log"))
#     for file_name in file_list:
#         with open(file_name, "r") as file:
#             for line in file:
#                 # 分割每行数据，以空格或制表符为分隔符
#                 data = line.split()
#                 # 如果该行有数据
#                 if data:
#                     # 获取第一列数据
#                     column_data = float(data[4]) / float(data[5]) / 1000
#                     # 打印第一列数据
#                     ret.append(column_data)
#     # print(len(ret)) 带宽数据长度是3345
#     for each_b in ret:
#         if each_b < 0.5:
#             each_b += 0.5
#     return ret


def alg_run(t_slo, R, c, Band):
    # 导入带宽数据

    # 初始化serverless端的三元组
    l_i = []
    bi = [1, 2, 3, 4, 5, 10, 15, 20]
    mi = [1024, 2048, 3072, 4096]
    j_selected = 999
    # 计数器，是第i个三元组的编号，也即配置编号

    # 初始化边缘端的延迟数据
    # 之前选取的边界值意义：一般来说请求是大量的，所以队列等待时间随batch大小增加的很慢。但是推理延迟增长地很快。
    # 所以batch大小有一个上限 不能超过这个值
    # 在边缘端batchsize在1~1000之内都是可选的
    # 成本的意义是把一秒内到达的请求全部推理完毕之后所花掉的价格
    b_0j = [1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100,200]
    # k是比值，以下是算法开头的排序过程
    N0 = []
    # for b0 in b_0j:
    #     l_0j.append(fitFunEdge(b0))
    # for j in range(0, len(b_0j)):
    #     k.append(l_0j[j] / b_0j[j])
    count = 0
    for j in b_0j:
        N0.append([])
        N0[count].append(j)
        N0[count].append(fitFunEdge(j))
        N0[count].append(fitFunEdge(j) / j)
        count += 1
    # 添加完毕开始按比值排序
    # 可以搞成l b 比值三元组，按比值的值进行排序，再分割
    # print(list(result))
    # 用sorted按比值排序
    # res = sorted(N0, key=lambda x: x[2])
    # 按绝对延迟降序排序，提高GPU利用率
    res = sorted(N0, key=lambda x: x[0], reverse=True)
    # print(res)
    # 排序完毕，再拆开分
    b0j = [j[0] for j in res]
    l0j = [j[1] for j in res]
    kj = [j[2] for j in res]
    for lll in l0j:
        if lll <= t_slo / 2:
            # for j in range(0, len(b_0j)):
            for j in range(0, len(b_0j)):
                if fitFunEdge(b_0j[j]) == lll:
                    j_selected = j
                    break
            break
    if j_selected == 999:
        print("t_slo设置的太小，edge端已有数据无法满足要求")
    else:
        print("edge可用最大临界batch size：%d" % b_0j[j])
        print("临界请求rps：%d" % (2 * b_0j[j_selected] / t_slo))
        print(f"/当前总rps：{R}")

    # 这里选出的是原来数组的d下标
    # 算法主体if开始
    # 这个值用于求出R2的阈值，并非采取的配置
    if R <= 2 * b_0j[j_selected] / t_slo:

        R2 = R

        #     老办法排序选最佳的，先做出目标延迟
        k2 = []
        count = 0
        N0 = []
        for j in b_0j:
            N0.append([])
            N0[count].append(j)
            N0[count].append(fitFunEdge(j))
            N0[count].append(fitFunEdge(j) + j / R2)
            count += 1
        # for j in range(0, len(b_0j)):
        #     k2.append(l_0j[j] + b_0j[j] / R2)
        #     合并成三元组。如果求索引的话其实二元组就够了
        # 用sorted按比值排序
        # print(N0)
        # 按绝对延迟降序排序，提高GPU利用率
        res2 = sorted(N0, key=lambda x: x[0], reverse=True)
        # 排序完毕，再拆开分
        b0j2 = [j[0] for j in res2]
        l0j2 = [j[1] for j in res2]
        kj2 = [j[2] for j in res2]
        for j in range(0, len(b0j2)):
            # b_0是最后要输出的值
            if b0j2[j] > 1 and l0j2[j] + b0j2[j] / R2 <= t_slo and l0j2[j] <= b0j2[j] / R2:
                b_0 = b0j2[j]
                break
            if b0j2[j] == 1 and l0j2[j] <= t_slo:
                b_0 = b0j2[j]
                break
        # with open("allocation2.txt", 'a') as f:
        #     f.write(str(t_slo) + ' ' + str(R) + ' ' + str(b_0) + ' ' + 'edge' + '\n')
        print(f"未能超过临界bs，只使用edge")
        # if b_0j[j] == 1:
        #     print("bs=1，不用排队")
        #     print(f"edge的余裕时间为{t_slo - l0j2[j]}\n")
        # else:
        #     print(f"edge的排队时间为{b_0 / R2}\n")
        #     print(f"edge的余裕时间为{t_slo - l0j2[j] - b_0 / R2}\n")
        print(f"选用edge的bs为{b_0}")
        return b_0
    else:
        b_0 = b_0j[j_selected]
        R2 = 2 * b_0j[j] / t_slo
        R1 = R - R2
        # if b_0j[j] == 1:
        #     print("bs=1，不用排队")
        # else:
        #     print(f"edge的排队时间为{b_0j[j] / R2}\n")
        # print(f"edge的余裕时间为{t_slo - l0j[j] - b_0j[j] / R2}\n")
        print(f"R1大小为{R1}")
        # 依旧是排序，但现在要变成四元组了，解决了这一步代码也就写完了
        count = 0
        Ni = []
        for i1 in bi:
            for i2 in mi:
                Ni.append([])
                Ni[count].append(i1)
                Ni[count].append(i2)
                Ni[count].append(fitFunServerless(i1, i2))
                Ni[count].append(c * i2 * fitFunServerless(i1, i2) * math.ceil(R1 / i1))
                # 上行是成本，目前总是选择batchsize=1，最好让它倾向于选择bs大的
                # 虽然bs增大后实例数量会减少，但是推理时间几乎也是成倍增长，导致成本反而增加
                # 应该还是拟合函数有问题，serverless的代码那里目前还是串行。重新再拟合一下
                count += 1
        # 三元组创建完毕,准备按成本排序
        res3 = sorted(Ni, key=lambda x: x[3])
        # 排序结束,
        for i in res3:
            if i[0] > 1 and i[2] + i[0] / R1 + fitTransTime(i[0], Band) <= t_slo:
                x = i
                # print(f"serverless的排队时间为{x[0] / R1}\n")
                print(f"传输时间为{fitTransTime(i[0], Band)}")
                # print(f"serverless的余裕时间为{t_slo - x[2] - fitTransTime(x[0], Band) - x[0] / R1}\n")
                break
            elif i[0] == 1 and i[2] + fitTransTime(i[0], Band) <= t_slo:
                print(f"传输时间为{fitTransTime(i[0], Band)}")
                # print(f"serverless的余裕时间为{t_slo - i[2] - fitTransTime(i[0], Band)}")
                x = i
                break
        # with open("allocation2.txt", 'a') as f:
        #     f.write(str(t_slo) + ' ' + str(R) + ' ' + str(b_0) + ' ' + str(x[0]) + ' ' + str(
        #         x[1]) + ' ' + 'edge+serverless' + ' ' + str(x[3]) + '\n')
        print(f"选用edge的bs为{b_0}")
        print(f"选用serverless的bs是{x[0]}，内存是{x[1]}，推理延迟是{x[2]}，该批次成本为{x[3]}元")
        print(f"当前带宽是{Band}MB/s")
        return b_0, x[0], x[1]
    # 返回三元组，分别是edge的bs、serverless的bs、serverless的内存


#     到此算法结束
if __name__ == "__main__":
    ans = alg_run(0.8, 300, 0.0000127 / 1024, 2.857)

    # print(ans)
    # t_slo = 0.8
    # R = 60
    # c = 0.0000127 / 1024
    # Band = 2.857
