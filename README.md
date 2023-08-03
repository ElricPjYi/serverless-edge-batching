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

```bash
# edge side preparing
python main.py

# client side
python 
```

## Usage Example

Below is an example demonstrating how to use the scheduling engine:
(If you have completed the allocation of your machine learning application on your edge device and serverless platform:)
```python
# client side

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


