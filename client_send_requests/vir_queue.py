import time
from threading import Thread
import alg
import requests
import glob
import send111
import test_orin_post
# 循环测试
# for i in range(10):
#   send111.sendrequest(20,2048)
import json

log = print


# 获取带宽trace


def send_batch(url, batchsize, size, base_env):
    file_datas = []

    # send package format
    batch_data = {
        "batchsize": batchsize,
        "size": size,
        "file-type": "image",
        "data": file_datas,
        "isBase64Encoded": True
    }

    # send across HTTP
    json_data = json.dumps(batch_data)
    headers = {"content-type": "application/json"}
    # r = requests.post(url, headers=headers, data=json_data)
    if base_env == "EDGE":
        infTime = test_orin_post.send_edge(batchsize)
        log(f"*************inference time on <EDGE>:<{infTime}>*************")
    if base_env == "SERVERLESS":
        infTime = send111.sendrequest(batchsize)
        log(f"-------------inference time on <SERVERLESS>:<{infTime}>-------------")
    # log(r.status_code)
    # log(r.json())
    # return r.json()
    return infTime


def send_batch_isolated(url, batchsize, size, env):
    t = Thread(target=send_batch, args=(url, batchsize, size, env))
    t.start()


# def freshConfig():
#     t = Thread(target=freshConfig_isolated, args=())
#     t.start()


class VQueue:
    def __init__(self, BatchSize=20, BatchSizeS=2, Memory=1024, SLO=0.8, Timeout=0.4):
        self.BatchSize = BatchSize
        self.BatchSizeS = BatchSizeS

        self.Memory = Memory
        self.SLO = SLO
        self.Timeout = Timeout

        self.R_status = 0
        self.interval = []
        self.bandwidth = []
        self.interval_pointer = 0
        self.interval_pointer_read = 0  # 用来计算rps，原先的方法不可取，rps太大
        self.bandwidth_pointer = 0
        self.rps_pointer = 0
        self.rps_pointer_read = 0

        self.url = "http://192.168.123.101:5000"
        self.loadInterval()
        self.loadBandwidth()
        self.rps = 0
        self._running = True  # 表示trace是否已经读取完毕，控制配置更新的定时器的停止

    def loadInterval(self, fileName='workload/workload-3.json'):
        with open(fileName, 'r') as f:
            self.interval = json.load(f)

    def loadBandwidth(self, fileName='bandwidth.json'):
        with open(fileName, 'r') as f:
            self.bandwidth = json.load(f)

    def send(self, env):
        if env == "EDGE":
            length = self.BatchSize
            wait_time = 0
            count = 0

            for i in range(length):
                if wait_time + self.interval[self.interval_pointer] <= self.Timeout:
                    wait_time += self.interval[self.interval_pointer]
                    self.interval_pointer += 1
                    count += 1
                else:
                    break
            log(f'Prepare <{self.BatchSize}> requests')
            log(f'Actual send <{count}> requests to <{env}>')
            log(f'wait_time/timeout = <{wait_time}>/<{self.Timeout}>')
            time.sleep(wait_time)

            send_batch_isolated(self.url, self.BatchSize, count, env)
        if env == "SERVERLESS":
            length = self.BatchSizeS
            wait_time = 0
            count = 0

            for i in range(length):
                if wait_time + self.interval[self.interval_pointer] <= self.Timeout:
                    wait_time += self.interval[self.interval_pointer]
                    self.interval_pointer += 1
                    count += 1
                else:
                    break
            log(f'Prepare <{self.BatchSizeS}> requests')
            log(f'Actual send <{count}> requests to <{env}>')
            log(f'wait_time/timeout = <{wait_time}>/<{self.Timeout}>')
            time.sleep(wait_time)

            send_batch_isolated(self.url, self.BatchSizeS, count, env)

    def freshConfig_isolated(self):
        while self._running:
            time.sleep(5)
            print("++++++++++++++++ALG RUNNING+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            # rps_avg_list = self.rps[self.rps_pointer_read:self.rps_pointer]
            # print(rps_avg_list)
            # if len(rps_avg_list) != 0:
            # rps_avg = sum(rps_avg_list) / len(rps_avg_list)
            self.rps_pointer_read = self.rps_pointer
            print(f"++++++++++++++++++++++GOT AVERAGE RPS: {self.rps}+++++++++++++++++++++++++++++++++++++++")
            alg_res = alg.alg_run(self.SLO, self.rps, 0.0000127 / 1024, self.bandwidth[self.bandwidth_pointer])


            if not isinstance(alg_res, int):

                self.BatchSize = alg_res[0]
                self.BatchSizeS = alg_res[1]
                if self.Memory != alg_res[2]:
                    send111.update_s(alg_res[2])
                    self.Memory = alg_res[2]
                    print(
                        "++++++++++++++++MEMORY UPDATE COMPLETE++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                with open("update_log.txt", "a") as f:
                    f.write(f"{alg_res[0]} {alg_res[1]} {alg_res[2]} {self.rps}\n" )
            else:
                self.BatchSize = alg_res
                self.BatchSizeS = 0
                with open("update_log.txt", "a") as f:
                    f.write(f"{alg_res} 0 0 {self.rps}\n")
            print("+++++++++++++++++++++++++++++++UPDATE COMPLETE+++++++++++++++++++++++++++++++++++++++")
            # else:
            #     print("==============请求轨迹读取结束========================")
            #     return
            # 求过一次平均值之后，前面的数据就不需要了，直接从此刻开始计算下一段trace的平均值
            self.bandwidth_pointer += 5

    def freshRPS(self):
        # 蔡深版
        # while self.rps_pointer <= self.interval_pointer:
        #     interval = self.interval[self.rps_pointer]
        #     if interval == 0:
        #         # 间隔为 0, rps 设置和前面一样
        #         self.rps.append(self.rps[-1])
        #     else:
        #         self.rps.append(1 / interval)
        #     self.rps_pointer += 1
        if self.interval_pointer_read < self.interval_pointer:
            rps_avg_list = self.interval[self.interval_pointer_read:self.interval_pointer]
            self.rps = len(rps_avg_list) / sum(rps_avg_list) * 2 # 改变数值以提高多样性
            self.interval_pointer_read = self.interval_pointer
        else:
            print("轨迹读取完毕，无需再次刷新当前时段rps")

    def run(self):
        # while True and (self.interval_pointer + self.BatchSize < len(self.interval)):
        # freshConfig() # 不确定放在这个位置对不对
        start_flag = 0
        th = Thread(target=self.freshConfig_isolated, args=())
        th.start()
        while True and (self.interval_pointer + self.BatchSize < 4000):
            self.send("EDGE")
            self.send("SERVERLESS")
            self.freshRPS()
            if start_flag == 0:
                th = Thread(target=self.freshConfig_isolated, args=())
                th.start()
                start_flag = 1

        self._running = False
        # 子线程定时执行配置更新
        # self.freshConfig()


def test_virtual_queue(BatchSize=20, BatchSizeS=2, Memory=1024, SLO=1, Timeout=0.4):
    vq = VQueue(BatchSize, BatchSizeS, Memory, SLO, Timeout)
    # vq.send()
    # vq.freshConfig()
    vq.run()


if __name__ == "__main__":
    # main()
    # test()
    test_virtual_queue()
