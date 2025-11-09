# Fullstack AWS Launch App

A comprehensive full-stack cloud project built with AWS services. This repository covers ECS, EC2, and DevOps fundamentals to deploy, manage, and scale containerized applications using modern cloud-native practices.

## About This Project

This repository contains the code and resources for a full-stack project designed to be built and deployed entirely on AWS. It appears to be structured as a learning course, with each directory representing a different module or stage of the application's development and deployment.

The project walks through key concepts, from building a local API and gateway to containerizing them with Docker and deploying them to scalable AWS services like EC2 and ECS.

## Technologies Used

* **Backend:** Python, Flask
* **Containerization:** Docker
* **Cloud Platform:** Amazon Web Services (AWS)
* **Core AWS Services:** Amazon EC2, Amazon ECS

## Project Structure

This repository is broken down into several key modules:

* **/Building the API**: Contains the source code for the core backend API.
* **/Building the Gateway Application**: Contains the code for a gateway service that interacts with the API.
* **/Deploy API on Docker**: Includes Dockerfiles and configurations to containerize the API.
* **/Composing the System**: Likely contains `docker-compose` files or scripts to run the multi-container application locally.
* **/AWS_deployment**: Contains infrastructure-as-code (IaC) scripts, configuration files, and guides for deploying the application to AWS.
* **/common**: Appears to hold shared code or utilities used by other modules.
* **/Introduction**: A starting point or overview for the project.

## How to Use This Repository

It is recommended to explore the directories in order, as they appear to build upon each other.

### 1. Prerequisites

Before you begin, ensure you have the following tools installed on your local machine:
* [Python 3.x](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [AWS CLI](https://aws.amazon.com/cli/) (configured with your AWS credentials)
* [Git](https://git-scm.com/downloads/)

### 2. Installation & Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/aliagasiyev/fullstack-aws-launch-app.git](https://github.com/aliagasiyev/fullstack-aws-launch-app.git)
    cd fullstack-aws-launch-app
    ```

2.  **Explore each module:**
    * Each module (e.g., `Building the API`) will likely have its own set of dependencies.
    * You may need to install Python packages for each part. Look for a `requirements.txt` file in the directories:
        ```bash
        # Example for one of the modules
        pip install -r "Building the API/requirements.txt"
        ```

3.  **Run with Docker (Locally):**
    * Navigate to the modules related to Docker and Composing (e.g., `Deploy API on Docker`, `Composing the System`).
    * Use Docker commands to build and run the containers as specified in those modules.
        ```bash
        # Example command, adjust based on the project's files
        docker-compose up --build
        ```

### 3. AWS Deployment

To deploy this application to the cloud, follow the instructions and use the scripts located in the `/AWS_deployment` directory. This will guide you through provisioning the necessary AWS resources (like EC2 instances or ECS clusters) to run your containerized application.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
