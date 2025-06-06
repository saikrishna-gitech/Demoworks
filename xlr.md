Here's a clear step-by-step guide to document image/container deployment using Jenkins and XLR (XL Release) for OpenShift:


---

📄 Overview

This process outlines how to automate container image builds and deployments to OpenShift using Jenkins for CI and XLR for orchestrating CD.


---

🧩 Components Used

Jenkins – for building and pushing images

XLR (XL Release) – for orchestrating deployment pipelines

OpenShift – for running containerized workloads

Image Registry – e.g., Docker Hub or OpenShift internal registry



---

🔧 1. Jenkins Setup

a. Build & Push Docker Image

Jenkins Pipeline (e.g., Jenkinsfile):

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-app'
        IMAGE_TAG = 'v1.0'
        REGISTRY = 'image-registry.openshift-image-registry.svc:5000/myproject'
    }

    stages {
        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push to OpenShift Registry') {
            steps {
                sh """
                docker login -u openshift -p $(oc whoami -t) $REGISTRY
                docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                """
            }
        }

        stage('Notify XLR') {
            steps {
                script {
                    // HTTP call or plugin to trigger XLR
                    sh 'curl -X POST http://xlr.example.com:5516/api/v1/releases -H "Authorization: Bearer <token>" -d @xlr_payload.json'
                }
            }
        }
    }
}


---

🚀 2. XLR (XL Release) Configuration

a. Create a Release Template

Define stages: e.g., Image Promotion, Deployment Approval, OpenShift Deployment


b. Add Tasks

1. Jenkins Build Trigger (Optional)


2. Gate (Approval if needed)


3. OpenShift Deployment Task:

Use XLR plugin or oc CLI via script to deploy:


oc rollout restart deployment/my-app -n myproject

Or apply YAML:

oc apply -f deployment.yaml




---

☸️ 3. OpenShift Configuration

a. ImageStream & DeploymentConfig

Example:

apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: my-app
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: my-app
        image: image-registry.openshift-image-registry.svc:5000/myproject/my-app:v1.0


---

🔄 4. End-to-End Flow

1. Developer commits code → triggers Jenkins.


2. Jenkins builds & pushes image.


3. Jenkins triggers XLR via REST API or plugin.


4. XLR orchestrates release and deploys to OpenShift using defined tasks.


5. Application updated in OpenShift with new image.




---

✅ Best Practices

Use webhooks for triggering.

Add approval gates in XLR for production stages.

Integrate with Vault for secrets (if needed).

Use ConfigMaps/Secrets for environment-specific configs.



---

Would you like a downloadable doc/pdf or a diagram of this flow?

