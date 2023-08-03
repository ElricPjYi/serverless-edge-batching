# # coding:utf-8
# 这是发送给serverless的代码
import json
import os
# import grequests

import time
import bandwidth
import sys
import shutil

from typing import List

from alibabacloud_fc_open20210406.client import Client as FC_Open20210406Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_fc_open20210406 import models as fc__open_20210406_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


# 把这个发送部分弄成函数 sendRequest(batch_size, placement)

# def __init__(self):
#     pass

# @staticmethod
def create_client(
        access_key_id: str,
        access_key_secret: str,
) -> FC_Open20210406Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'your_url'
    return FC_Open20210406Client(config)


#

# 本地测试

# orin/NX测试

# 云测试

# 初始化每个batch的文件列表
# def sendrequest(batch_size,mem):
def sendrequest(batch_size):
    if batch_size == 0:
        print("-------------------rps不高，暂时不启动serverless----------------")
        return
    files = []
    # 打开目录，选中全部图片
    imageList = os.listdir('test1')
    # 设定好一个请求是一张图片
    images_num = 1
    # 开始之前，把上次测试的result.txt删掉
    if os.path.exists('result.txt'):
        os.remove('result.txt')
    # 一个请求包含images_num张图片，循环准备一定数量的请求
    # 配置信息
    # batch_size = 20
    # memory=32768
    req_list = []
    client = create_client('your-access-key', 'your-access-key-password')
    runtime = util_models.RuntimeOptions()
    # rps=10
    # 以下为测试并发用的代码，如果是基于rps则不需要这些
    # 制作请求列表，以便同时发送
    # for num in range(batch_size):
    #     # 准备请求内的一定数目的图片
    #     imageList_b = imageList[num*images_num:(num+1)*images_num]
    #     for each_image in imageList_b:
    #         t = ("images", (each_image, open(os.path.join('test1', each_image), 'rb').read()))
    #         files.append(t)
    #     # 制作请求，添加到列表
    #     re = grequests.post(url, files=files)
    #     req_list.append(re)
    #     # 下一个请求之前清空files列表
    #     files = []
    # # 请求列表制作完毕，同时发送请求,计算等待时间
    # start_time=time.time()
    # res_list = grequests.map(req_list)
    # end_time=time.time()
    # 为返回结果设置一个空列表
    # # 获取内存信息
    # get_function_headers = fc__open_20210406_models.GetFunctionHeaders()
    # get_function_request = fc__open_20210406_models.GetFunctionRequest()
    # res2 = client.get_function_with_options('test1', 'image2', get_function_request, get_function_headers, runtime)
    # 更新函数内存大小

    # update_function_headers = fc__open_20210406_models.UpdateFunctionHeaders()
    # update_function_request = fc__open_20210406_models.UpdateFunctionRequest(
    #     memory_size=mem
    # )
    # client.update_function_with_options('test1', 'image2', update_function_request, update_function_headers, runtime)
    # time.sleep(2)
    # 循环测试数据中！待会删掉！
    for z in range(1):
        start_time = time.time()
        # for i in range(batch_size):
        #     # 准备请求内的一定数目的图片
        #     imageList_b = imageList[i * images_num:(i+1) * images_num]
        #     # print(imageList_b)
        #     for each_image in imageList_b:
        #         t = ("images", (each_image, open(os.path.join('test1', each_image), 'rb').read()))
        #         files.append(t)
        # res_json = requests.post(url, files=files)

        invoke_function_headers = fc__open_20210406_models.InvokeFunctionHeaders()
        invoke_function_request = fc__open_20210406_models.InvokeFunctionRequest(
            body=UtilClient.to_bytes(batch_size)
        )
        # 请求体内容可以从data里面找到 真nm太坑了
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.invoke_function_with_options('test1', 'image2', invoke_function_request,
                                                      invoke_function_headers, runtime)

        #  print(res.body.decode()) # bytes类型转字符串,这里永远是字符串类型
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
        # files=[]
        # #清空队列 不然总是乱发 而且会发的越来越多
        # print(res_json.text)
        # res = json.loads(res_json.text)

        # res_list=res['res']
        # inf_time =res['latency']
        # res_list=res.get('res')
        # print(res_list)
        # inf_time=res.get('latency')
        # time.sleep(0.1)
        # # 下一个请求之前清空files列表、结果列表
        # res_list = []
        # files = []
        end_time = time.time()
        # 5s等待足够返回结果
        time.sleep(5)
        time_ans = (float(res.headers["x-fc-invocation-duration"])) / 1000
        # print('batch size为%d ' % batch_size + '内存为%d ' % mem + '响应时间为%s秒 ' % (
        #             end_time - start_time) + '推理时间为%f秒' % time_ans)
        # print('batch size为%d ' % batch_size +  '响应时间为%s秒 ' % (
        #             end_time - start_time) + '推理时间为%f秒' % time_ans)
        # print('\n')
        # # print(type())
        # print('推理结果为%s' % res.body)

        # 最后一个请求运行完才可以开始写结果
        # with open('result.txt','w') as f:
        #     # for num in range(rps):
        #     #     f.write('######################\n')
        #     #     f.write('The request '+str(num)+'\'s result is:\n\n\n')
        #     #     f.write(res_list[num].text+'\n')
        #         f.write('######################\n')
        #         f.write('The request '+'\'s result is:\n\n\n')
        #         f.write(res_list+'\n')
        #
        with open('fitting_api_new.txt', 'a') as f:
            f.write(str(batch_size))
            f.write(' ')
            f.write(str(3072))
            f.write(' ')
            f.write(str(time_ans))
            f.write('\n')
        # print(f"推理时间为{time_ans}")
        return time_ans
        # for i i n range(int(batch_size)):
        #     shutil.copyfile('1.jpg', 'images\\%d.jpg'%i)
        # all_images = os.listdir('images')
        # print(all_images)


# 更新serverless上的内存信息，会有一定延迟
def update_s(memory):
    client = create_client('your-access-key', 'your-access-key-password')
    runtime = util_models.RuntimeOptions()
    update_function_headers = fc__open_20210406_models.UpdateFunctionHeaders()
    update_function_request = fc__open_20210406_models.UpdateFunctionRequest(
        memory_size=memory
    )
    client.update_function_with_options('test1', 'image2', update_function_request, update_function_headers, runtime)


if __name__ == "__main__":
    # main()
    # test()
    sendrequest(1)
