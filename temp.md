Here’s a sample XLR (XL Release) template to deploy a Python image to an OpenShift cluster. This template uses the Kubernetes plugin or Custom Script task to trigger oc CLI commands to deploy the image.


---

🔧 Assumptions

You have a Service Account Token or kubeconfig set up for authentication.

You are deploying a Docker image to a specific namespace.

The image is already pushed to an accessible image registry (e.g., DockerHub, Quay, OpenShift internal registry).

oc CLI is installed and available on the agent.



---

✅ XLR Template YAML

apiVersion: xl-release/v1
kind: Template
metadata:
  name: Deploy Python App to OpenShift
  description: Deploy a Python image to OpenShift using oc CLI
spec:
  phases:
    - name: Deploy to OpenShift
      tasks:
        - name: Login to OpenShift
          type: xlrelease.ScriptTask
          script: |
            echo "Logging into OpenShift"
            oc login https://${openshift_api_url} --token=${openshift_token} --insecure-skip-tls-verify

        - name: Apply Deployment YAML
          type: xlrelease.ScriptTask
          script: |
            echo "Deploying Python image to OpenShift"
            cat <<EOF | oc apply -f -
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: ${deployment_name}
              namespace: ${namespace}
            spec:
              replicas: 1
              selector:
                matchLabels:
                  app: ${deployment_name}
              template:
                metadata:
                  labels:
                    app: ${deployment_name}
                spec:
                  containers:
                  - name: python-container
                    image: ${image_url}
                    ports:
                    - containerPort: 5000
            EOF

        - name: Expose Service
          type: xlrelease.ScriptTask
          script: |
            oc expose deployment ${deployment_name} --port=5000 --name=${deployment_name}-svc -n ${namespace}
            oc expose svc/${deployment_name}-svc -n ${namespace}

        - name: Verify Deployment
          type: xlrelease.ScriptTask
          script: |
            echo "Checking rollout status"
            oc rollout status deployment/${deployment_name} -n ${namespace}


---

📥 Template Variables

Ensure the following variables are defined in the release:

Variable Name	Description

openshift_api_url	OpenShift API endpoint URL
openshift_token	Access token for authentication
namespace	Namespace to deploy the app
deployment_name	Name of the deployment
image_url	Full path of the Docker image



---

✅ Example Values

openshift_api_url: api.openshift.example.com:6443
openshift_token: sha256~abc123xyz
namespace: python-apps
deployment_name: my-python-api
image_url: quay.io/myorg/python-api:latest


---

Would you like me to provide this as a downloadable .yaml file or importable XLR template archive?

