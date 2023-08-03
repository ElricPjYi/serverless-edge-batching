# serverless-edge-batching

Cloud-Edge Collaborative Batch Processing Request Scheduling Engine based on Serverless

## Project Description

This project is a machine learning inference request scheduling engine developed in Python for the Linux environment. It is designed to be deployed on Serverless and edge devices. After deploying the inference models, the engine dynamically merges inference requests into different batches based on the current network bandwidth and request arrival rate. It intelligently decides the task computation scenarios to reduce costs and improve response speed.

## Key Features

- Implements model deployment on servers and edge devices using Flask and triggers function execution with Serverless.
- Sets up a **virtual queue** to buffer incoming requests and utilizes timers to record individual request and overall batch waiting timeouts.
- **Designs algorithms** to ensure that inference latency does not exceed batch waiting latency and selects the most economical instance configuration.
- Determines task offloading locations based on fitting **inference latency and data transmission speed (Bandwidth)**.
- Utilizes **Bayesian changepoint detection algorithm** to reduce unnecessary scheduling status update overhead.

## Requirements

- Linux operating system
- Python
- Flask framework
- Serverless platform support (Ali)

## Installation and Running

1. Clone the project to your local machine:

```bash
git clone https://github.com/ElricPjY/serverless-edge-batching.git
cd serverless-edge-batching
```

2. Install the required dependencies:
```bash
flask
imageai==3.0.3
pillow>=7.0.0 
numpy>=1.18.1
opencv-python>=4.1.2 
torch>=1.9.0 
--extra-index-url https://download.pytorch.org/whl/cu102 
torchvision>=0.10.0 
--extra-index-url https://download.pytorch.org/whl/cu102 
pytest==7.1.3 
tqdm==4.64.1 
scipy>=1.7.3 
matplotlib>=3.4.3 
mock==4.0.3

```

3. Run the application:
The defualt settings (BatchSize==edge, BatchSizeS==serverless):
```python
BatchSize=20, BatchSizeS=2, Memory=1024, SLO=1, Timeout=0.4
```

```bash
# edge side preparing
python main.py

# client side
# first we need to test the GPU
python test_orin_post.py

# then we can start
python vir_queue.py
```

## Usage Example

Below is an example demonstrating how to use the scheduling engine:
(If you have completed the allocation of your machine learning application on your edge device and serverless platform:)
```python
# client side
Prepare <20> requests
Actual send <20> requests to <EDGE>
wait_time/timeout = <0.380278487>/<0.4>
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.02320671>/<0.4>
Prepare <20> requests
Actual send <20> requests to <EDGE>
wait_time/timeout = <0.326456749>/<0.4>
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.072288>/<0.4>
Prepare <20> requests
Actual send <20> requests to <EDGE>
wait_time/timeout = <0.30455148>/<0.4>
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.0498661>/<0.4>
Prepare <20> requests
Actual send <18> requests to <EDGE>
wait_time/timeout = <0.38748677>/<0.4>
*************inference time on <EDGE>:<0.4342057704925537>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.0513268>/<0.4>
Prepare <20> requests
Actual send <15> requests to <EDGE>
wait_time/timeout = <0.386950571>/<0.4>
*************inference time on <EDGE>:<0.43500566482543945>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.01885679>/<0.4>
Prepare <20> requests
Actual send <19> requests to <EDGE>
wait_time/timeout = <0.390669124>/<0.4>
*************inference time on <EDGE>:<0.2891998291015625>*************
*************inference time on <EDGE>:<0.18002080917358398>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.0164201>/<0.4>
Prepare <20> requests
Actual send <19> requests to <EDGE>
wait_time/timeout = <0.39697051299999997>/<0.4>
*************inference time on <EDGE>:<0.16693830490112305>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.00656733>/<0.4>
Prepare <20> requests
Actual send <18> requests to <EDGE>
wait_time/timeout = <0.39796082699999996>/<0.4>
*************inference time on <EDGE>:<0.17467331886291504>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.0334782>/<0.4>
Prepare <20> requests
Actual send <14> requests to <EDGE>
wait_time/timeout = <0.39858447999999996>/<0.4>
*************inference time on <EDGE>:<0.1643073558807373>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.02087332>/<0.4>
*************inference time on <EDGE>:<0.16253900527954102>*************
Prepare <20> requests
Actual send <18> requests to <EDGE>
wait_time/timeout = <0.3408898000000001>/<0.4>
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.1776868>/<0.4>
*************inference time on <EDGE>:<0.16440773010253906>*************
Prepare <20> requests
Actual send <15> requests to <EDGE>
wait_time/timeout = <0.3942432127>/<0.4>
*************inference time on <EDGE>:<0.1619558334350586>*************
Prepare <2> requests
Actual send <2> requests to <SERVERLESS>
wait_time/timeout = <0.020466980000000003>/<0.4>
Prepare <20> requests
Actual send <20> requests to <EDGE>
wait_time/timeout = <0.3955086920000001>/<0.4>
++++++++++++++++ALG RUNNING+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++GOT AVERAGE RPS: 81.98496347205888+++++++++++++++++++++++++++++++++++++++
edge可用最大临界batch size：50
临界请求rps：100
/当前总rps：81.98496347205888
未能超过临界bs，只使用edge
选用edge的bs为40
+++++++++++++++++++++++++++++++UPDATE COMPLETE+++++++++++++++++++++++++++++++++++++++


# edge side log
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on {ip}
 * Running on {ip}
Press CTRL+C to quit
2.4686057567596436
192.168.123.28 - - [02/Aug/2023 19:45:41] "POST / HTTP/1.1" 200 -
0.17660832405090332
192.168.123.28 - - [02/Aug/2023 19:45:42] "POST / HTTP/1.1" 200 -
0.1535181999206543
192.168.123.28 - - [02/Aug/2023 19:45:42] "POST / HTTP/1.1" 200 -
0.1298506259918213
192.168.123.28 - - [02/Aug/2023 19:45:43] "POST / HTTP/1.1" 200 -
0.12336373329162598
192.168.123.28 - - [02/Aug/2023 19:45:43] "POST / HTTP/1.1" 200 -
0.3576805591583252
192.168.123.28 - - [02/Aug/2023 19:45:57] "POST / HTTP/1.1" 200 -
0.2634620666503906
192.168.123.28 - - [02/Aug/2023 19:45:57] "POST / HTTP/1.1" 200 -
0.17376184463500977
192.168.123.28 - - [02/Aug/2023 19:45:57] "POST / HTTP/1.1" 200 -
0.16669225692749023
192.168.123.28 - - [02/Aug/2023 19:45:58] "POST / HTTP/1.1" 200 -
0.17017579078674316
192.168.123.28 - - [02/Aug/2023 19:45:58] "POST / HTTP/1.1" 200 -
0.16566085815429688

```

## Contribution

We welcome contributions, feedback, and suggestions for this project. If you wish to contribute, please feel free to submit a Pull Request, and we'll review it promptly.


## Author

- Author: Your Name
- GitHub: [Your GitHub Profile](https://github.com/your_username)

## Acknowledgments

We extend our gratitude to the following projects for their inspiration and support:

- [Flask](https://flask.palletsprojects.com/)
- [Ali Function Compute Serverless Platform](https://www.aliyun.com/product/fc)


