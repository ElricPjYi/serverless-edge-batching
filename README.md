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
git clone https://github.com/your_username/project.git
cd project
```

2. Install the required dependencies:

```bash
pip install flask
# Additional steps to install Serverless dependencies
```

3. Run the application:

```bash
python app.py
```

## Usage Example

Below is an example demonstrating how to use the scheduling engine:

```python
# Import necessary modules
from engine import Scheduler

# Create a scheduler instance
scheduler = Scheduler()

# Set up model deployment and Serverless functions
scheduler.setup_model_deployment()

# Start the scheduler
scheduler.start()
```

## Contribution

We welcome contributions, feedback, and suggestions for this project. If you wish to contribute, please feel free to submit a Pull Request, and we'll review it promptly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Author: Your Name
- GitHub: [Your GitHub Profile](https://github.com/your_username)

## Acknowledgments

We extend our gratitude to the following projects for their inspiration and support:

- [Flask](https://flask.palletsprojects.com/)
- [Serverless Platform](https://www.serverless.com/)

## Frequently Asked Questions

If you have any questions, please refer to our [FAQ](FAQ.md).

---
Note: The above README is a simple template. Please adjust and expand it according to your actual project details.
