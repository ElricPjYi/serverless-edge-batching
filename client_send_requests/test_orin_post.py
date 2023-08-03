import os
import time

import requests


def send_edge(batch_size):
    # batch_size = 500
    url = "http://192.168.123.101:5000"
    res = requests.post(url="http://192.168.123.101:5000", data={"bs": str(batch_size)})
    return res.text
if __name__ == "__main__":
    # main()
    # test()
    for i in range(5):
        send_edge(15)
# files = []
# # 打开目录，选中全部图片
# imageList = os.listdir('test1')
# images_num = 1
# # for z in range(1):
# #     start_time = time.time()
# #     for i in range(batch_size):
# #         # 准备请求内的一定数目的图片
# #         imageList_b = imageList[i * images_num:(i + 1) * images_num]
# #         # print(imageList_b)
# #         for each_image in imageList_b:
# #             t = ("images", (each_image, open(os.path.join('test1', each_image), 'rb').read()))
# #             files.append(t)
# #     res_json = requests.post(url, files=files)
