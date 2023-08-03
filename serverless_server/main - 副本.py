# coding:utf-8
from imageai.Classification import ImageClassification
from flask import request, Flask
import time
import os
import json
import shutil

app = Flask(__name__)


# 加载模型

@app.route("/", methods=['POST'])
def get_frame():
    # 加载模型：ResNet50
    start_time = time.time()
    execution_path = os.getcwd()
    prediction = ImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth"))
    prediction.loadModel()

    upload_file = request.files.getlist('images')
    images_path = 'images'
    if upload_file:
        print(upload_file)
        for each_file in upload_file:
            old_file_name = each_file.filename
            file_path = os.path.join(images_path, old_file_name)
            each_file.save(os.path.join(execution_path, file_path))
        print("success")
        print('file saved to %s' % images_path)

        print('Downloading duration:[%.0fms]' % ((time.time() - start_time) * 1000))
        # 读取收到的图片，无需设为列表（由于imageAI的更新，多图像预测已经失效）
        # 循环打印结果
        # all_images_array = []

        all_images = os.listdir(images_path)
        # 开始逐张图片推理，并将推理结果写入文本文档
        count = 0
        with open('./result.txt', 'w') as f:
            for each_image in all_images:
                predictions, probabilities = prediction.classifyImage(os.path.join(images_path, each_image),
                                                                      result_count=5)
                f.write('The image' + str(count) + ':\n')
                for eachPrediction, eachProbability in zip(predictions, probabilities):
                    # print(eachPrediction, " : ", eachProbability)
                    f.write(str(eachPrediction) + " : " + str(eachProbability) + '\n')
                f.write("-----------------------\n")
                count += 1
        with open('./result.txt', 'r') as f1:
            r = f1.read()
        count = 0
        durationtime = time.time() - start_time
        dic = {'res': r, 'latency': durationtime}
        res_json = json.dumps(dic)
        # 把收到的文件清掉
        shutil.rmtree('images')
        os.mkdir('images')
        return res_json

    else:
        return 'failed'


# @app.route("/", methods=['GET'])
# def give_result():
#     with open('./result.txt', 'r') as f:
#         r = f.read()
#     return r


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
    # orin 上说这个5000端口被占用了，换一个试试看
