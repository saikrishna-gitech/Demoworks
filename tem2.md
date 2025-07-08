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